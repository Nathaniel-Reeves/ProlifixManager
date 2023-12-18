'''
Handle Inventory Data
'''
import json
from flask import (
    Blueprint,
    request,
    jsonify
)
from .auth import check_authenticated
from .helper import only_integers
from .response import CustomResponse
from controller import catalogue as cat

bp_comp = Blueprint('components', __name__, url_prefix='/components')


@bp_comp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_components():
    custom_response = CustomResponse()
    
    custom_response = cat.get_components(custom_response)

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response

bp_cat = Blueprint('catalogue', __name__, url_prefix='/catalogue')
bp_cat.register_blueprint(bp_comp)