
import functools
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

bp = Blueprint('auth', __name__, url_prefix='/auth')

from server.models import auth


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            error = auth.register(username, password)

        flash(error)
        session.commit()

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = auth.login(username, password)
        if error:
            flash(error)
        else:
            return render_template("home/index.html")

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = auth.get_user(user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))

def check_privileges(privileges):
    if g.user["access_privileges"] == privileges:
        return True
    return False


