
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ..db import DatabaseConnection

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = DatabaseConnection()
        session = db.get_session()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                session.sql(
                    "INSERT INTO `Organizations`.`User` (`Username`, `Encrypted_Password`, `Manger_Privileges`, `Admin_Privileges`, `Recovery_Email`) VALUES (?, ?, 0, 0, \"TEST EMAIL\")",
                ).bind((username, generate_password_hash(password)),).execute()
            except Exception as err:
                if err.args[0] == 1062:
                    error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
        session.commit()

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        print("TEST")
        username = request.form['username']
        print("USERNAME = ", username)
        password = request.form['password']
        db = DatabaseConnection()
        error = None
        user = db.sql(
            'SELECT * FROM `Organizations`.`User` WHERE `Username` = ?'
        ).bind((username,)).execute().fetch_one()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['Encrypted_Password'], password):
            error = 'Incorrect password.'
        print("ERROR = ", error)
        if error is None:
            session.clear()
            session['User_ID'] = user['User_ID']
            return redirect(url_for('home.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('User_ID')

    if user_id is None:
        g.user = None
    else:
        db = DatabaseConnection()
        g.user = db.sql(
            'SELECT * FROM `Organizations`.`User` WHERE `User_ID` = ?'
        ).bind((user_id,)).execute().fetch_one()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
