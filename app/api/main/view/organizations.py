'''
Handle Organizations Endpoints
'''
import json
from flask import (
    Blueprint,
    request,
    jsonify
)
from controller import organizations as org
from .auth import check_authenticated
from .helper import only_integers, check_type
from .response import CustomResponse

bp = Blueprint('organizations', __name__, url_prefix='/organizations')

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_organizations():
    """
    GET api/organizations/ Endpoint
    """

    # Clean Request
    org_ids = list(only_integers(request.args.getlist('org-id')))

    types_request = request.args.getlist('org-type')
    valid_types = [
        'client',
        'supplier',
        'lab',
        'courier'
    ]
    org_types = check_type(valid_types, types_request)

    populate_request = request.args.getlist('populate')
    valid_populate = [
        'facilities',
        # 'sales_orders',
        # 'purchase_orders',
        'people',
        'components',
        'products',
        'organization_names'
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

    # Get Organizations from the database
    custom_response = CustomResponse()
    custom_response = org.get_organizations(
        custom_response,
        org_ids,
        org_types,
        populate,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response

@bp.route('/facilities', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_facilities():
    """
    GET api/organizations/ Endpoint
    """

    # Clean Request
    facility_ids = list(only_integers(request.args.getlist('facility_id')))

    org_ids = list(only_integers(request.args.getlist('org_id')))

    # types_request = request.args.getlist('facility_type')
    # valid_types = [
    #     'Head_Office',
    #     'Office',
    #     'Distribution_Warehouse',
    #     'Manufacturing_Warehouse',
    #     'Storefront'
    # ]
    # facility_types = check_type(valid_types, types_request)

    populate_request = request.args.getlist('populate')
    valid_populate = [
        'organizations'
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

    # Get Organizations from the database
    custom_response = CustomResponse()
    custom_response = org.get_facilities(
        custom_response,
        facility_ids,
        org_ids,
        populate,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response


@bp.route('/people', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_people():
    """
    GET api/organizations/ Endpoint
    """

    # Clean Request
    person_ids = list(only_integers(request.args.getlist('person_id')))

    org_ids = list(only_integers(request.args.getlist('org_id')))

    # types_request = request.args.getlist('org-type')
    # valid_types = [
    #     'client',
    #     'supplier',
    #     'lab',
    #     'courier'
    # ]
    # org_types = check_type(valid_types, types_request)

    populate_request = request.args.getlist('populate')
    valid_populate = [
        'users',
        'organizations'
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

    # Get Organizations from the database
    custom_response = CustomResponse()
    custom_response = org.get_people(
        custom_response,
        person_ids,
        org_ids,
        populate,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response
