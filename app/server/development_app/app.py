from flask import Flask, jsonify
from flask_cors import CORS
import configparser

# Database Config Settings
config = configparser.ConfigParser()
config.read('config.ini')
HOST = config.get('database', 'HOST')
PORT = int(config.get('database', 'PORT'))
USER = config.get('root', 'MYSQL_ROOT_USERNAME')
PASSWORD = config.get('root', 'MYSQL_ROOT_PASSWORD')

print('~~~ DATABASE CONFIG ~~~')
print('    Host:         ', HOST)
print('    Port:         ', PORT)
print('    SQL User:     ', USER)
print('    SQL Password: ', PASSWORD)
print()


"""
Config Settings for Flask App
"""
app = Flask(__name__, instance_relative_config=True)

CORS(app, resources={r'/*': {'origins': '*'}})

"""
Import Views
"""
# from server.views.home import bp as home_bp
# app.register_blueprint(home_bp)

# from server.views.auth import bp as auth_bp
# app.register_blueprint(auth_bp)

# from server.views.organizations import bp as organizations_bp
# app.register_blueprint(organizations_bp)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == "__main__":
    print('~~~ SERVER START ~~~')
    print()
    app.run(debug=True, port=5001)
