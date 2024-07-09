'''
Handle all requests to interact with data in the database.
'''
from flask import (
    Blueprint,
    request,
    jsonify
)
from .auth import check_authenticated
from controller.order_66 import order_66

bp = Blueprint('order_66', __name__, url_prefix='/order_66')

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_submit():
    res = order_66(request)
    response = jsonify(res.to_json())
    response.status_code = res.get_status_code()
    return response
