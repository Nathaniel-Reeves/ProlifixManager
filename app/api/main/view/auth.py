'''
Handle Authentication Rules for Users
'''
import functools
import json
import random
import string
import sys
import os
import mariadb
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app as app,
    make_response
)
from redis import (
    Redis,
    RedisError
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from .response import (
    MessageType,
    Message,
    FlashMessage,
    CustomResponse,
    error_message
)

def get_session_token(request):
    # This funciton was made to make mocking easier for unittests.
    session_token = request.cookies.get('session')
    return session_token

# Login & Authenication Wrapper Functions

def check_authenticated(authentication_required=False, database_priveleges=None):
    """
    Check if the user is authenticated.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            try:
                custom_response = CustomResponse()  # Create an instance of Response

                redis_connection = Redis(
                    host=app.config['REDIS_HOST'],
                    port=app.config['REDIS_PORT'],
                    password=app.config['REDIS_PASSWORD'],
                    socket_connect_timeout=1)
                
                redis_connection.ping()

                # Check if user has a session token, Create one if not
                session_token = get_session_token(request)
                print(session_token)
                
                if (session_token is None) or (not redis_connection.exists(session_token)):
                    session_token = create_session()
                    if isinstance(session_token, FlashMessage):
                        custom_response.insert_flash_message(session_token)
                        return jsonify(custom_response.to_json()), 500

                    else:
                        message = FlashMessage(
                            message='New Session Token Created',
                            message_type=MessageType.SUCCESS
                        )
                        custom_response.insert_flash_message(message)

                raw_session_data = redis_connection.get(session_token)
                session_data = json.loads(raw_session_data)

                # Check if User is Authenticated
                if authentication_required and not session_data['user_id']:
                    custom_response.insert_flash_message(
                        FlashMessage(
                            message='User not authenticated',
                            message_type=MessageType.DANGER
                        )
                    )
                    response = make_response(
                        jsonify(custom_response.to_json()), 401)
                    response.set_cookie('session', session_token)
                    return response

                response = func(*args, **kwargs)
                response.set_cookie('session', session_token)
                return response

            except RedisError as error:
                # Redis Error Handling
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                custom_response.insert_flash_message(
                    FlashMessage(
                        alert_heading='Redis Error',
                        message="Redis Server Error",
                        message_detail=str(error),
                        message_type=MessageType.DANGER,
                        dismissible=False,
                        debug_code=f"Error:{exc_type} > File: {fname} > Line: {exc_tb.tb_lineno}"
                    )
                )
                response = jsonify(custom_response.to_json())
                response.status_code = custom_response.get_status_code()
                return response

        return wrapper

    return decorator

def create_session():
    """
    Create a new blank session.
    """

    # Create Session Template
    user_data_template = {
        "department": "",
        "doc": {},
        "first_name": "",
        "job_description": "",
        "last_name": "",
        "organization_id": 0,
        "person_id": 0,
        "profile_picture": "",
        "user_id": "",
        "username": ""
    }

    # Generate Random Session token
    session_token = ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(32)])

    # Save Session to Redis
    try:
        redis_connection = Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'],
            socket_connect_timeout=1
            )
        redis_connection.ping()
        redis_connection.set(session_token, json.dumps(user_data_template))
        redis_connection.expire(
            session_token, app.config['SESSION_EXPIRE'], nx=False, xx=False, gt=False, lt=False)
        return session_token

    except RedisError as error:
        # Redis Error Handling
        return FlashMessage(message=str(error),
                            message_type=MessageType.DANGER)


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/sessions', methods=['POST'])
def login():
    """
    Checks if user exists in DB, if so login user
    by updating the session cookie and storing session in
    redis and sending cookie to user.
    """
    custom_response = CustomResponse()  # Create an instance of Response

    # Get username and password
    username = request.json['username']
    password = request.json['password']

    # Check if user exists in DB
    try:
        # Test Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOST'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )

        # Build Query
        base_query = '''
        SELECT
            JSON_OBJECT(
                'user_id', a.`user_id`,
                'person_id', a.`person_id`,
                'username', a.`username`,
                'encrypted_password', a.`encrypted_password`,
                'profile_picture', a.`profile_picture`,
                'doc', a.`doc`,
                'organization_id', b.`organization_id`,
                'first_name', b.`first_name`,
                'last_name', b.`last_name`,
                'job_description', b.`job_description`,
                'department', b.`department`
            )
        AS user_objects
        FROM `Organizations`.`Users` a
        LEFT JOIN `Organizations`.`People` b ON
            a.`person_id` = b.`person_id`
        WHERE a.`username` = ?
        '''

        # Execute Query
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, (username,))
        result = cursor.fetchone()

        # Handle User Exists
        user_data = None
        if result:
            user_data = json.loads(result[0])
        else:
            custom_response.insert_form_message(
                "username", Message(message="User not found",
                             message_type=MessageType.DANGER)
            )
            return jsonify(custom_response.to_json()), 401

        # Handle Check Password
        if not check_password_hash(user_data['encrypted_password'], password):
            custom_response.insert_form_message(
                "password", Message(message="Incorrect Password",
                             message_type=MessageType.DANGER)
            )
            return jsonify(custom_response.to_json()), 401

        # Remove Encrypted Password from user_data
        user_data.pop("encrypted_password", None)

        # Check if user has a session token, Create one if not
        session_token = get_session_token(request)
        redis_connection = Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'],
            socket_connect_timeout=1
            )
        redis_connection.ping()
        if (session_token is None) or (not redis_connection.exists(session_token)):
            session_token = create_session()
            if isinstance(session_token, FlashMessage):
                custom_response.insert_flash_message(session_token)
                return jsonify(custom_response.to_json()), 500

        session_data = json.loads(redis_connection.get(session_token))

        # Update Session Data
        session_data['user_id'] = user_data['user_id']
        session_data['person_id'] = user_data['person_id']
        session_data['username'] = user_data['username']
        session_data['profile_picture'] = user_data['profile_picture']
        session_data['doc'] = user_data['doc']
        session_data['organization_id'] = user_data['organization_id']
        session_data['first_name'] = user_data['first_name']
        redis_connection.set(session_token, json.dumps(session_data))
        redis_connection.expire(
            session_token, app.config['SESSION_EXPIRE'], nx=False, xx=False, gt=False, lt=False)

        # Insert the user_data & cookie into the response
        custom_response.insert_data(user_data)
        response = make_response(
            jsonify(custom_response.to_json()), 201)
        response.set_cookie('session', session_token)
        return response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()


@bp.route('/sessions', methods=['GET'])
def get_user_by_session_token():
    """
    Get User by the Session Token from Redis
    """
    session_token = request.args.get('session-token', default=None, type=str)

    try:
        custom_response = CustomResponse()  # Create an instance of Response
        status_code = 200

        redis_connection = Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'],
            socket_connect_timeout=1
            )
        redis_connection.ping()
        if redis_connection.exists(session_token):
            user_data = json.loads(redis_connection.get(session_token))
            custom_response.insert_data(user_data)
            return jsonify(custom_response.to_json()), 200
        else:
            custom_response.insert_flash_message(
                FlashMessage(message="User not authenticated",
                             message_type=MessageType.DANGER))
            status_code = 401
            new_session_token = create_session()
            response = make_response(jsonify(custom_response.to_json()), status_code)
            response.set_cookie('session', new_session_token)
            return response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500

@bp.route('/sessions', methods=['DELETE'])
@check_authenticated(authentication_required=True)
def logout():
    """
    Logs user out of the session.
    """

    try:
        session_token = get_session_token(request)
        status_code = 401
        if session_token is not None:
            redis_connection = Redis(
                host=app.config['REDIS_HOST'],
                port=app.config['REDIS_PORT'],
                password=app.config['REDIS_PASSWORD'],
                socket_connect_timeout=1
                )
            redis_connection.ping()
            result = redis_connection.getdel(session_token)
            custom_response = CustomResponse()
            if result is not None:
                custom_response.insert_flash_message(
                    FlashMessage(message="User successfully logged out",
                                 message_type=MessageType.SUCCESS))
                status_code = 200
            else:
                custom_response.insert_flash_message(
                    FlashMessage(message="User not authenticated",
                                 message_type=MessageType.DANGER))
        else:
            custom_response.insert_flash_message(
                FlashMessage(message="User not authenticated",
                             message_type=MessageType.DANGER))

        response = jsonify(custom_response.to_json())
        response.status_code = custom_response.get_status_code()
        return response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500
