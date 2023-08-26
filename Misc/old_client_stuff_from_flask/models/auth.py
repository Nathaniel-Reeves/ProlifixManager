
import mysqlx
from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)
from flask import session as client_session

from server.db import init_db


def register(username, password):
    session = init_db()
    try:
        session.sql(
            "INSERT INTO `Organizations`.`Users` (`person_id`, `username`, `encrypted_password`, `access_privileges`) VALUES (?, ?, ?, ?)",
        ).bind((username, generate_password_hash(password)),).execute()
    except Exception as err:
        if err.args[0] == 1062:
            error = f"User {username} is already registered."
    session.close()
    return error

def login(username, password):
    db_session = init_db()
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
    db_session.close()
    return error

def get_user(user_id):
    session = init_db()
    data = session.sql(
        'SELECT * FROM `Organizations`.`Users` WHERE `user_id` = ?'
    ).bind((user_id,)).execute().fetch_one()
    session.close()
    return data

