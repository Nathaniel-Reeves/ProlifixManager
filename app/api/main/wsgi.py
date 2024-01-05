"""
Creates App Instance
"""
from datetime import timedelta
import socket
import os
import sys
from flask import (
    Flask,
    jsonify,
    Blueprint
)
from flask_cors import CORS
from flask_socketio import SocketIO
from dotenv import load_dotenv

# Get the parent directory
parent_dir = os.path.dirname(os.path.realpath(__file__))

# Add the parent directory to sys.path
sys.path.append(parent_dir)

def print_config():
    print()
    print("App Configurations:")
    for v in env_variables:
        print(f"    {v[0]}: {v[1]}")
    print()
    print()

# Set env variables
print("Loading Environment Variables")
app_dir = os.path.split(os.path.split(parent_dir)[0])[0]
print(f"Env Location: ", os.path.join(app_dir,".env"))
load_dotenv(os.path.join(app_dir,".env"), override=True)
env_variables = os.environ.items()
print_config()

def create_app():
    
    app = Flask(__name__)

    """
    Database Connection Settings
    """
    app.config['DB_HOST'] = os.environ.get('DB_HOST')
    app.config['DB_PORT'] = os.environ.get('DB_PORT')
    app.config['DB_USER'] = os.environ.get('DB_USER')
    app.config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD')
    
    """
    File Settings
    """
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    if UPLOAD_FOLDER == "DEFAULT":
        project_dir = os.path.split(os.getcwd())[0]
        app.config['UPLOAD_FOLDER'] = os.path.join(project_dir, 'db/files')
    else:
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = ("application/pdf")

    """
    Redis Connection Settings
    """
    app.config['REDIS_HOST'] = os.environ.get('REDIS_HOST')
    app.config['REDIS_PORT'] = os.environ.get('REDIS_PORT')
    app.config['REDIS_PASSWORD'] = os.environ.get('REDIS_PASSWORD')
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = False
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_EXPIRE'] = timedelta(days=7)
    app.config['ALLOWED_EXTENSIONS'] = (".pdf")

    CORS(app, supports_credentials=True, allow_headers=[
        "Content-Type", "Access-Control-Allow-Origin"])



    # login_manager = LoginManager(app)
    # flask_jwt_conf = JWTManager(app)
    # server_session = Session(app)
    socketio = SocketIO(app, manage_session=False)

    #  Set the API prefix to a falsey (empty string) value to
    #  send/recive traffic from the development client,
    #  $ export API_PREFIX=
    
    API_PREFIX = os.environ.get('API_PREFIX')
    if API_PREFIX == 'True':
        API_PREFIX = '/'
    else:
        API_PREFIX = '/api/v1'


    api_blueprint = Blueprint('api', __name__, url_prefix=API_PREFIX)


    """
    Import Old Controler
    """
    from old_controler.orders import bp as orders_bp
    api_blueprint.register_blueprint(orders_bp)

    # from old_controler.inventory import bp as inventory_bp
    # api_blueprint.register_blueprint(inventory_bp)
    
    """
    Import Views
    """
    from view.organizations import bp as organizations_bp
    api_blueprint.register_blueprint(organizations_bp)
    
    from view.catalogue import bp_cat as catalogue_bp
    api_blueprint.register_blueprint(catalogue_bp)
    
    from view.auth import bp as auth_bp
    api_blueprint.register_blueprint(auth_bp)

    """
    Sanity Check Routes
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

    return app

if __name__ == "__main__":
    load_dotenv(override=True)
    print_config()
    app = create_app()
    print('~~~ SERVER START ~~~')
    app.run(
        debug=True, 
        port=5000, 
        host="0.0.0.0"
    )
