'''
Handle Organizations Data
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
from controller import organizations as org

bp = Blueprint('organizations', __name__, url_prefix='/organizations')

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_organizations():
    """
    GET api/organizations/ Endpoint
    """

    # Clean Request
    org_ids = list(only_integers(request.args.getlist('org-id')))

    org_types_request = request.args.getlist('org-type')
    org_types = []
    if 'client' in org_types_request:
        org_types.append('client')
    if 'supplier' in org_types_request:
        org_types.append('supplier')
    if 'lab' in org_types_request:
        org_types.append('lab')
    if 'courier' in org_types_request:
        org_types.append('courier')
    if len(org_types) == 4:  # Empty list means get all org types
        org_types = []

    populate_request = request.args.getlist('populate')
    populate = []
    if 'facilities' in populate_request:
        populate.append('facilities')
    if 'sales-orders' in populate_request:
        populate.append('sales-orders')
    if 'purchase-orders' in populate_request:
        populate.append('purchase-orders')
    if 'people' in populate_request:
        populate.append('people')
    if 'components' in populate_request:
        populate.append('components')
    if 'products' in populate_request:
        populate.append('products')
        
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

@bp.route('/exists', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_org_exists():
    """
    Check if an organization already exists by organization name.
    """
    custom_response = CustomResponse()  # Create an instance of Response

    names = request.json['names']

    custom_response = org.organization_exists(names, custom_response)
    
    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response