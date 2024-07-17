'''
Handle Inventory Data
'''
from flask import (
    Blueprint,
    request,
    jsonify
)
from .auth import check_authenticated
from .helper import only_integers, check_type
from .response import CustomResponse
from controller import inventory as inv
from controller import products as prod

bp_cat = Blueprint('catalogue', __name__, url_prefix='/catalogue')
bp_comp = Blueprint('components', __name__, url_prefix='/components')
bp_prod = Blueprint('products', __name__, url_prefix='/products')

@bp_comp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_components():
    """
    GET api/v/catalogue/components/ Endpoint
    """

    # Clean Request
    component_ids = list(only_integers(request.args.getlist('component-id')))

    process_component_ids = list(only_integers(request.args.getlist('process-component-id')))

    types_request = request.args.getlist('type')
    valid_types = [
        'powder', 'liquid', 'container', 'pouch','shrink_band',
        'lid', 'label', 'capsule','misc','scoop', 'desiccant',
        'box', 'carton', 'packaging_material'
    ]
    component_types = check_type(valid_types, types_request)

    certifications_request = request.args.getlist('certification')
    valid_certifications = [
        'usda_organic',
        'halal',
        'kosher',
        'gluten_free',
        'national_sanitation_foundation',
        'us_pharmacopeia',
        'non_gmo',
        'vegan',
        'wildcrafted',
        'made_with_organic',
        'gmp',
        'fda'
    ]

    certifications = check_type(
        valid_certifications,
        certifications_request,
        empty_means_all=False
    )

    brand_ids = list(only_integers(request.args.getlist('brand-id')))

    populate_request = request.args.getlist('populate')
    valid_populate = [
        'purchase_order_detail',
        'inventory',
        'brand',
        'component_names'
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

    custom_response = inv.get_components(
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

@bp_prod.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_products():
    """
    GET api/v/catalogue/products/ Endpoint
    """

    # Clean Request
    product_ids = list(only_integers(request.args.getlist('product-id')))

    certifications_request = request.args.getlist('certification')
    valid_certifications = [
        'usda_organic',
        'halal',
        'kosher',
        'gluten_free',
        'national_sanitation_foundation',
        'us_pharmacopeia',
        'non_gmo',
        'vegan',
        'wildcrafted',
        'made_with_organic',
        'gmp',
        'fda'
    ]

    certifications = check_type(
        valid_certifications,
        certifications_request,
        empty_means_all=False
    )

    client_ids = list(only_integers(request.args.getlist('client-id')))

    populate_request = request.args.getlist('populate')
    valid_populate = [
        'lot-numbers',
        'inventory',
        'formulas',
        'components',
        'manufacturing',
        'product_variants'
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

    # Get Products from Database
    custom_response = CustomResponse()

    custom_response = prod.get_products(
        custom_response,
        product_ids,
        certifications,
        client_ids,
        populate,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response

bp_cat.register_blueprint(bp_comp)
bp_cat.register_blueprint(bp_prod)
