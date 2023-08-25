"""
Creates App
"""
from datetime import timedelta
import socket
import os
from flask import (
    Flask,
    jsonify,
    Blueprint
)
from flask_cors import CORS
from flask_socketio import SocketIO

"""
Database Connection Settings
"""

DB_HOST = os.environ.get('DB_HOST')
if DB_HOST is None:
    DB_HOST = '172.10.10.2'

DB_PORT = os.environ.get('DB_PORT')
if DB_PORT is None:
    DB_PORT = '3306'

DB_USER = os.environ.get('DB_USERNAME')
if DB_USER is None:
    DB_USER = 'client'

DB_PASSWORD = os.environ.get('DB_PASSWORD')
if DB_PASSWORD is None:
    DB_PASSWORD = "ClientPassword!5"

os.chdir("..")
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'db/files')
os.chdir("server")

print()
print('~~~ DATABASE CONFIG ~~~')
print('    Host:         ', DB_HOST)
print('    Port:         ', DB_PORT)
print('    SQL User:     ', DB_USER)
print('    SQL Password: ', DB_PASSWORD)
print('    Upload Folder: ', UPLOAD_FOLDER)
print()

"""
Redis Connection Settings
"""
REDIS_HOST = os.environ.get('REDIS_HOST')
if REDIS_HOST is None:
    REDIS_HOST = "172.10.10.3"

REDIS_PORT = os.environ.get('REDIS_PORT')
if REDIS_PORT is None:
    REDIS_PORT = 6379

REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD')
if REDIS_PASSWORD is None:
    REDIS_PASSWORD = "Am^7qq?%QgedcLn"

print()
print('~~~ REDIS CONFIG ~~~')
print('    Host:         ', REDIS_HOST)
print('    Port:         ', REDIS_PORT)
print('    Password:     ', REDIS_PASSWORD)
print()

API_PREFIX = os.environ.get('API_PREFIX')
if API_PREFIX == 'True':
    API_PREFIX = '/'
else:
    API_PREFIX = '/api'

print()
print('~~~ API CONFIG ~~~')
print('    API Prefix:   ', API_PREFIX)
print()

"""
Config Settings for Flask App
"""


def create_app(
        DB_HOST=DB_HOST, 
        DB_PORT=DB_PORT, 
        DB_USER=DB_USER, 
        DB_PASSWORD=DB_PASSWORD, 
        REDIS_HOST=REDIS_HOST, 
        REDIS_PORT=REDIS_PORT, 
        REDIS_PASSWORD=REDIS_PASSWORD, 
        UPLOAD_FOLDER=UPLOAD_FOLDER,
        API_PREFIX=API_PREFIX
    ):

    app = Flask(__name__)

    app.config['DB_HOSTNAME'] = DB_HOST
    app.config['DB_PORT'] = DB_PORT
    app.config['DB_USER'] = DB_USER
    app.config['DB_PASSWORD'] = DB_PASSWORD
    app.config['REDIS_HOST'] = REDIS_HOST
    app.config['REDIS_PORT'] = REDIS_PORT
    app.config['REDIS_PASSWORD'] = REDIS_PASSWORD
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_EXPIRE'] = timedelta(days=7)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = (".pdf")

    CORS(app, supports_credentials=True, allow_headers=[
        "Content-Type", "Access-Control-Allow-Origin"])

    app.secret_key = '0kgy23uJpIin346NeC7hUZ3Bak36S844NoeN1X35k4kY'


    # login_manager = LoginManager(app)
    # flask_jwt_conf = JWTManager(app)
    # server_session = Session(app)
    socketio = SocketIO(app, manage_session=False)

    #  Set the API prefix to a falsey (empty string) value to
    #  send/recive traffic from the development client,
    #  $ export API_PREFIX=


    api_blueprint = Blueprint('api', __name__, url_prefix=API_PREFIX)


    """
    Import Handlers
    """
    from handlers.organizations import bp as organizations_bp
    api_blueprint.register_blueprint(organizations_bp)

    from handlers.orders import bp as orders_bp
    api_blueprint.register_blueprint(orders_bp)

    from handlers.auth import bp as auth_bp
    api_blueprint.register_blueprint(auth_bp)

    from handlers.inventory import bp as inventory_bp
    api_blueprint.register_blueprint(inventory_bp)

    """
    sanity check routes
    """

    @api_blueprint.route('/ping', methods=['GET'])
    def ping_pong():
        """
        ping pong route
        """

        return jsonify('pong!')

    @api_blueprint.route('/server_id', methods=['GET'])
    def server_id():
        """
        server id route
        """

        return f"Container ID: {socket.gethostname()}"

    # @api_blueprint.route('/redis')
    # def hello():
    #     redis.incr('hits')
    #     counter = str(redis.get('hits'), 'utf-8')
    #     return "Welcome to this webpage!, This webpage has been viewed "+counter+" time(s)"

    app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app = create_app()
    print('~~~ SERVER START ~~~')
    app.run(debug=True, port=5000, host="0.0.0.0")
