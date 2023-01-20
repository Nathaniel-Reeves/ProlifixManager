from mrp_app import app


def allowed_file(filename, allowed_extensions=app.config["ALLOWED_EXTENSIONS"]):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions
