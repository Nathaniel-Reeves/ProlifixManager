from flask import Flask, jsonify
from flask_cors import CORS
import os

# Database Config Settings
HOST = os.environ.get('HOSTNAME')
PORT = os.environ.get('DB_PORT')
USER = os.environ.get('ROOT_USERNAME')
PASSWORD = os.environ.get('ROOT_PASSWORD')
API_PORT = int(os.environ.get('API_PORT'))
DEBUG_MODE = bool(os.environ.get('API_PORT'))

print('~~~ DATABASE CONFIG ~~~')
print('    Host:         ', HOST)
print('    Port:         ', PORT)
print('    SQL User:     ', USER)
print('    SQL Password: ', PASSWORD)
print('    API_PORT:     ', API_PORT)
print('    DEBUG_MODE:   ', DEBUG_MODE)
print()


"""
Config Settings for Flask App
"""
app = Flask(__name__, instance_relative_config=True)

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


if __name__ == "__main__":
    print('~~~ SERVER START ~~~')
    print()
    app.run(debug=DEBUG_MODE, port=5000, host="0.0.0.0")
