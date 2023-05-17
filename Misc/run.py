from flask import Flask, jsonify
from flask_cors import CORS

import functools
from flask import (
    g,
    redirect,
    url_for
)

"""
Config Settings for Flask App
"""
app = Flask(__name__, instance_relative_config=True)

CORS(app, resources={r'/*': {'origins': '*'}})

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

"""
Import Views
"""
from server.views.home import bp as home_bp
app.register_blueprint(home_bp)

from server.views.auth import bp as auth_bp
app.register_blueprint(auth_bp)

from server.views.organizations import bp as organizations_bp
app.register_blueprint(organizations_bp)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

if __name__ == "__main__":
    print('~~~ SERVER START ~~~')
    print()
    app.run(debug=True)
