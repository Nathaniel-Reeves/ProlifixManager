from flask import Flask, jsonify
from flask_cors import CORS
import os
import socket

# Redis session store notes
# https://testdriven.io/blog/flask-server-side-sessions/

# Database Config Settings

HOST = os.environ.get('DB_HOSTNAME')
if HOST is None:
    HOST = 'pi-server'

PORT = os.environ.get('DB_PORT')
if PORT is None:
    PORT = '3306'

USER = os.environ.get('DB_USERNAME')
if USER is None:
    USER = 'client'

PASSWORD = os.environ.get('DB_PASSWORD')
if PASSWORD is None:
    PASSWORD = "ClientPassword5!"

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

"""
Import Handlers
"""
from handlers.organizations import bp as organizations_bp
app.register_blueprint(organizations_bp)


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

# sanity check route
@app.route('/server_id', methods=['GET'])
def server_id():
    return f"Container ID: {socket.gethostname()}"


if __name__ == "__main__":
    print('~~~ SERVER START ~~~')
    app.run(debug=True, port=5000, host="0.0.0.0")
