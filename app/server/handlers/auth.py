import functools
import json
import random
import string
import mariadb
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app as app,
    make_response
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from flask_socketio import disconnect

"""
Login & Authenication Wrapper Functions
"""

def check_authenticated(
        authentication_required=False,
        database_priveleges={}
    ):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            # Check if user has a session token, Create one if not
            session_token = request.cookies.get('session')
            if session_token is None:
                session_token = create_session()
            session = app.config['SESSION_REDIS']
            if not session.exists(session_token):
                session_token = create_session()
            session_data = json.loads(session.get(session_token))

            # Check if User is Authenticated
            user_authenticated = False
            if session_data['user_id']:
                user_authenticated = True

            if authentication_required:
                if not user_authenticated:
                    response = make_response(
                        jsonify({'success': False, 'message': 'User not authenticated'}), 401)
                else:
                    response = func(*args, **kwargs)
            else:
                response = func(*args, **kwargs)

            response.set_cookie('session', session_token)
            return response
        return wrapper
    return decorator

def create_session():
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
    session = app.config['SESSION_REDIS']
    session.set(session_token, json.dumps(user_data_template))
    session.expire(session_token, int(app.config['SESSION_EXPIRE']))
    return session_token

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/sessions', methods=['POST'])
def login():
    """
    Checks if user exists in DB, if so login user
    by creating a session and storing session in 
    redis and sending cookie to user.
    """

    # Get username and password
    username = request.json['username']
    password = request.json['password']

    # Check if user exists in DB
    try:
        # Test Connection
        session = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
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
        cursor = session.cursor()
        cursor.execute(base_query, (username,))
        result = cursor.fetchone()

        # Handle User Exists
        user_data = None
        if result:
            user_data = json.loads(result[0])
        else:
            return make_response(jsonify({"error": "User not found"}), 401)

        # Handle Check Password
        if not check_password_hash(user_data['encrypted_password'], password):
            return make_response(jsonify({"error": "Incorrect Password"}), 401)
        
        # Remove Encrypted Password from user_data
        user_data.pop("encrypted_password", None)

        # Check if user has a session token, Create one if not
        session_token = request.cookies.get('session')
        if session_token is None:
            session_token = create_session()
        session = app.config['SESSION_REDIS']
        if not session.exists(session_token):
            session_token = create_session()
        session_data = json.loads(session.get(session_token))

        # Update Session Data
        session_data['user_id'] = user_data['user_id']
        session_data['person_id'] = user_data['person_id']
        session_data['username'] = user_data['username']
        session_data['profile_picture'] = user_data['profile_picture']
        session_data['doc'] = user_data['doc']
        session_data['organization_id'] = user_data['organization_id']
        session_data['first_name'] = user_data['first_name']
        session.set(session_token, json.dumps(session_data))

        return jsonify(user_data)

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return jsonify(error=str(error))

    finally:
        if 'session' in locals():
            session.close()


@bp.route('/sessions', methods=['GET'])
def get_user_by_session_token():
    session_token = request.args.get('session-token', default=None, type=str)

    session = app.config['SESSION_REDIS']
    if session.exists(session_token):
        user_data = json.loads(session.get(session_token))
        return jsonify(user_data)
    else:
        return make_response(jsonify({"error": "User not authenticated"}), 401)
