
from flask import send_from_directory

from server.run import app

@app.route('/uploads/<path:file_location>', methods=('GET', ))
def uploads(file_location):
    return send_from_directory(app["UPLOAD_FOLDER"], file_location)
