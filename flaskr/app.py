import os

from flask import Flask, send_from_directory, send_file
from werkzeug.utils import secure_filename
from . import db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.schema'),
    )

    app.config['UPLOAD_FOLDER'] = db.UPLOAD_FOLDER

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import handlers
    app.register_blueprint(handlers.auth.bp)
    app.register_blueprint(handlers.blog.bp)
    app.register_blueprint(handlers.home.bp)
    app.register_blueprint(handlers.hello.bp)
    app.register_blueprint(handlers.organizations.bp)

    @app.route('/uploads/<path:file_location>', methods=('GET', ))
    def uploads(file_location):
        print(db.UPLOAD_FOLDER)
        print(file_location)
        return send_from_directory(db.UPLOAD_FOLDER, file_location)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
