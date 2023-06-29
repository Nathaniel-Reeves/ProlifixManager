import functools
import json
from redis import Redis
import mariadb
from flask import (
    Blueprint,
    request,
    jsonify,
    request,
    current_app as app,
    make_response
)
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    set_access_cookies, 
    set_refresh_cookies,
    get_jwt,
    jwt_required,
    JWTManager
)
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from flask_socketio import disconnect
from flask_login import current_user, UserMixin

"""
Configure flask_jws_extended
"""

class User(UserMixin):

    def __init__(self):
        super(User, self).__init__()
        
    def get_id(self):
        return self.id

"""
Login & Authenication Wrapper Functions
"""

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # Check if user has a authenticated session
        if current_user.is_authenticated:
            return f(*args, **kwargs)
        else:
            return make_response(jsonify({
                'message': 'You must be logged in to access this resource.'
            }), 401)
    return wrapped


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

        # Create Session
        response = make_response(jsonify(user_data))
        access_token = create_access_token(identity=user_data['user_id'])
        refresh_token = create_refresh_token(identity=user_data['user_id'])

        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        session = app.config['SESSION_REDIS']
        session.set(username, json.dumps(user_data))
        session.expire(username, int(app.config['SESSION_EXPIRE']))

        # Send Cookie
        response = make_response(jsonify(user_data))
        response.set_cookie('session', username)
        return response

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return jsonify(error=str(error))

    finally:
        if 'session' in locals():
            session.close()
