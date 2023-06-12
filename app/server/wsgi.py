from flask import Flask, jsonify, Blueprint
from flask_cors import CORS
import os
import socket

# Redis session store notes
# https://testdriven.io/blog/flask-server-side-sessions/

# Database Config Settings

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
Config Settings for Flask App
"""
app = Flask(__name__)

app.config['DB_HOSTNAME'] = HOST
app.config['DB_PORT'] = PORT
app.config['DB_USER'] = USER
app.config['DB_PASSWORD'] = PASSWORD

CORS(app, supports_credentials=True, allow_headers=[
     "Content-Type", "Access-Control-Allow-Origin"])

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

# sanity check route
@api_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# sanity check route
@api_blueprint.route('/server_id', methods=['GET'])
def server_id():
    return f"Container ID: {socket.gethostname()}"


app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    print('~~~ SERVER START ~~~')
    app.run(debug=True, port=5000, host="0.0.0.0")
