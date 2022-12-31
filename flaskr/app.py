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
    def upload(file_location):
        file_location_list = os.path.normpath(file_location).split("/")
        filename = file_location_list.pop()
        sub_directories = ""
        for dir in file_location_list:
            sub_directories += dir + "/"
        return send_from_directory(os.path.join(db.UPLOAD_FOLDER, sub_directories), filename)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
