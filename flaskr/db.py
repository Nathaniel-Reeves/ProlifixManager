import mysqlx

import click
from flask import current_app, g
from flask.cli import with_appcontext

HOST = '192.168.1.42'
PORT = 33060
USER = 'client'
PASSWORD = 'clientPassword5!'

class DatabaseConnection():

    '''Database(database, table)
	arg:
		host (req) = hostname/ip address of mysql server
		user (req) = username of connection account
		password (req) = password of connection account
		database (opt) = name of database to connect to
		table (opt) = name of table to connect to
	Initializes a connection to a database.
	'''
    def __init__(self, host=HOST, port=PORT, user=USER, password=PASSWORD):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        
        # Connect to server on localhost
        self.session = mysqlx.get_session( {'host': self._host, 'port': self._port,'user': self._user, 'password': self._password } )
        
        return

    def get_session(self):
        return self.session

    def get_schema(self, schema):
        return self.session.get_schema(schema)

    def sql(self, sql):
        return self.session.sql(sql)

    def __del__(self):
        self.session.close()


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

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
