from flask import Flask, jsonify
from flask_cors import CORS
import os
import socket

# Database Config Settings
HOST = os.environ.get('HOSTNAME')
PORT = os.environ.get('DB_PORT')
USER = os.environ.get('ROOT_USERNAME')
PASSWORD = os.environ.get('ROOT_PASSWORD')

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

CORS(app, resources={r'/*': {'origins': '*'}})

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