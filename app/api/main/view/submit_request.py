'''
Handle all requests to interact with data in the database.
'''
from flask import (
    Blueprint,
    request,
    jsonify
)
from .auth import check_authenticated
from controller.request import CustomRequest, check_organization_levenshtein, check_component_levenshtein

bp = Blueprint('submit', __name__, url_prefix='/submit')

@bp.route('/', methods=['PUT'])
@check_authenticated(authentication_required=True)
def handle_submit():
    req = CustomRequest(request)
    req.handle_request()
    res = req.get_response()
    response = jsonify(res.to_json())
    response.status_code = res.get_status_code()
    return response

@bp.route('/check_organization', methods=['POST'])
@check_authenticated(authentication_required=True)
def check_organization():
    res = check_organization_levenshtein(request)
    response = jsonify(res.to_json())
    response.status_code = res.get_status_code()
    return response

@bp.route('/check_component', methods=['POST'])
@check_authenticated(authentication_required=True)
def check_component():
    res = check_component_levenshtein(request)
    response = jsonify(res.to_json())
    response.status_code = res.get_status_code()
    return response