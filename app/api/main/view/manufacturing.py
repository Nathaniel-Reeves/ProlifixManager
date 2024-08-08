'''
Handle Manufacturing Data
'''
from flask import (
    Blueprint,
    request,
    jsonify
)
from .auth import check_authenticated
from .helper import only_integers, check_type
from .response import CustomResponse
from controller import manufacturing as man

bp = Blueprint('processes', __name__, url_prefix='/processes')

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_processes():
    """
    GET api/v/processes/ Endpoint
    """

    # Clean Request
    process_ids = list(only_integers(request.args.getlist('process_id')))

    populate_request = request.args.getlist('populate')
    valid_populate = [
        'equipment'
    ]
    populate = check_type(
        valid_populate,
        populate_request,
        empty_means_all=False
    )

    doc = False
    document = request.args.get('doc')
    if document == "true":
        doc = True

    # Get Components from Database
    custom_response = CustomResponse()

    custom_response = man.get_processes(
        custom_response,
        process_ids,
        populate,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response