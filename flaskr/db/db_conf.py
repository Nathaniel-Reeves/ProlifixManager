

HOST = '192.168.1.42'
#HOST = 'localhost'
PORT = 33060
USER = 'client'
PASSWORD = 'clientPassword5!'
UPLOAD_FOLDER = '/mnt/c/Users/Nathaniel Reeves/Documents/uploads'
#UPLOAD_FOLDER = '/mnt/s/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


import click
from flask import current_app, g
from flask.cli import with_appcontext
import mysqlx


def allowed_file(filename, allowed_extensions=ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = mysqlx.get_session(
        {'host': HOST, 'port': PORT, 'user': USER, 'password': PASSWORD})

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)