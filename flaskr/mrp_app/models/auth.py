import functools
import mysqlx
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from flask import session as client_session

from mrp_app import app


def register(username, password):
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    try:
        session.sql(
            "INSERT INTO `Organizations`.`Users` (`person_id`, `username`, `encrypted_password`, `access_privileges`) VALUES (?, ?, ?, ?)",
        ).bind((username, generate_password_hash(password)),).execute()
    except Exception as err:
        if err.args[0] == 1062:
            error = f"User {username} is already registered."
    return error

def login(username, password):
    db_session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    error = None
    user = db_session.sql(
        'SELECT * FROM `Organizations`.`Users` WHERE `username` = ?'
    ).bind((username,)).execute().fetch_one()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['encrypted_password'], password):
        error = 'Incorrect password.'

    if error is None:
        client_session['user_id'] = user['user_id']

    return error

def get_user(user_id):
    session = mysqlx.get_session(app.config["DB_CREDENTIALS"])
    return session.sql(
        'SELECT * FROM `Organizations`.`Users` WHERE `user_id` = ?'
    ).bind((user_id,)).execute().fetch_one()

