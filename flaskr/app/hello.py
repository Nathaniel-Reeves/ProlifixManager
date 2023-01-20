from flask import (
    Blueprint,
    render_template,
)



bp = Blueprint('hello', __name__)


@bp.route('/')
def index():
    return render_template('hello/index.html')
