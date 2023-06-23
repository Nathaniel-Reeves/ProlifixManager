from flask import (
    Flask, 
    jsonify, 
    Blueprint
)
from redis import Redis
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session
from flask_socketio import SocketIO
import os
import socket

"""
Database Connection Settings
"""

HOST = os.environ.get('DB_HOSTNAME')
if HOST is None:
    HOST = '127.0.0.1'

PORT = os.environ.get('DB_PORT')
if PORT is None:
    PORT = '3306'

USER = os.environ.get('DB_USERNAME')
if USER is None:
    USER = 'client'

PASSWORD = os.environ.get('DB_PASSWORD')
if PASSWORD is None:
    PASSWORD = "ClientPassword!5"

print()
print('~~~ DATABASE CONFIG ~~~')
print('    Host:         ', HOST)
print('    Port:         ', PORT)
print('    SQL User:     ', USER)
print('    SQL Password: ', PASSWORD)
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

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

"""
Config Settings for Flask App
"""
app = Flask(__name__)

app.config['DB_HOSTNAME'] = HOST
app.config['DB_PORT'] = PORT
app.config['DB_USER'] = USER
app.config['DB_PASSWORD'] = PASSWORD
app.config['REDIS_HOST'] = REDIS_HOST
app.config['REDIS_PORT'] = REDIS_PORT
app.config['REDIS_PASSWORD'] = REDIS_PASSWORD
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis
app.config['SESSION_EXPIRE'] = 3600

CORS(app, supports_credentials=True, allow_headers=[
     "Content-Type", "Access-Control-Allow-Origin"])

app.secret_key = '0kgy23uJpIin346NeC7hUZ3Bak36S844NoeN1X35k4kY'
login_manager = LoginManager(app)

server_session = Session(app)
socketio = SocketIO(app, manage_session=False)

#  Set the API prefix to a falsey (empty string) value to 
#  send/recive traffic from the development client, 
#  $ export API_PREFIX=

#  Set the API prefix to a truthy (non-empty string) value
#  to send/recive traffic using postman & production client.
#  $ export API_PREFIX='True'
API_PREFIX = os.environ.get('API_PREFIX')
if API_PREFIX == 'True':
    url_prefix = '/'
else:
    url_prefix = '/api'

print()
print('~~~ API CONFIG ~~~')
print('    API Prefix:   ', API_PREFIX)
print()


api_blueprint = Blueprint('api', __name__, url_prefix=url_prefix)


"""
Import Handlers
"""
from handlers.organizations import bp as organizations_bp
api_blueprint.register_blueprint(organizations_bp)

from handlers.orders import bp as orders_bp
api_blueprint.register_blueprint(orders_bp)

from handlers.auth import bp as auth_bp
api_blueprint.register_blueprint(auth_bp)

"""
sanity check routes
"""

@api_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@api_blueprint.route('/server_id', methods=['GET'])
def server_id():
    return f"Container ID: {socket.gethostname()}"

@api_blueprint.route('/redis')
def hello():
    redis.incr('hits')
    counter = str(redis.get('hits'), 'utf-8')
    return "Welcome to this webpage!, This webpage has been viewed "+counter+" time(s)"

app.register_blueprint(api_blueprint)




if __name__ == "__main__":
    print('~~~ SERVER START ~~~')
    app.run(debug=True, port=5000, host="0.0.0.0")
