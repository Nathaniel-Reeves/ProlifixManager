
from flask import send_from_directory

from app import app
from db import db_conf as db

@app.route('/uploads/<path:file_location>', methods=('GET', ))
def uploads(file_location):
    return send_from_directory(db.UPLOAD_FOLDER, file_location)
