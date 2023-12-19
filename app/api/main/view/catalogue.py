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
from .helper import only_integers, check_type
from .response import CustomResponse
from controller import catalogue as cat

bp_comp = Blueprint('components', __name__, url_prefix='/components')


@bp_comp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_components():
    """
    GET api/v/catalogue/components/ Endpoint
    """

    # Clean Request
    component_ids = list(only_integers(request.args.getlist('component-id')))

    types_request = request.args.getlist('type')
    valid_types = [
        'powder', 'liquid', 'container', 'pouch','shrink-band', 'lid', 'label', 'capsule','misc','scoop', 'dessiccant', 'box', 'carton',
        'packaging-material'
    ]
    component_types = check_type(valid_types, types_request)
    
    certifications_request = request.args.getlist('certification')
    valid_certifications = [
        'usda-organic',
        'halal',
        'kosher',
        'gluten-free',
        'national-sanitation-foundation',
        'us-pharmacopeia',
        'non-gmo',
        'vegan'
    ]
    
    certifications = check_type(
        valid_certifications,
        certifications_request,
        empty_means_all=False
    )
    
    brand_ids = list(only_integers(request.args.getlist('brand-id')))
    
    populate_request = request.args.getlist('populate')
    valid_populate = [
        'product-materials',
        'purchase-order-detail',
        'label-formula-master',
        'ingredient-formula-detail',
        'item-id',
        'inventory',
        'brand'
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
    
    custom_response = cat.get_components(
        custom_response,
        component_ids,
        component_types,
        certifications,
        brand_ids,
        populate,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response

bp_cat = Blueprint('catalogue', __name__, url_prefix='/catalogue')
bp_cat.register_blueprint(bp_comp)