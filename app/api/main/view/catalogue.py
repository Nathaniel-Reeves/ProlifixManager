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
from .helper import only_integers, check_type, collect_form_data
from .response import CustomResponse, FlashMessage
from controller import inventory as inv
from controller import products as prod

bp_cat = Blueprint('catalogue', __name__, url_prefix='/catalogue')
bp_comp = Blueprint('components', __name__, url_prefix='/components')
bp_prod = Blueprint('products', __name__, url_prefix='/products')

@bp_comp.route('/', methods=['GET', 'POST', 'PUT'])
@check_authenticated(authentication_required=True)
def handle_components():

    if request.method == 'GET':
        return handle_get_components()
    elif request.method == 'POST':
        return handle_post_components()
    elif request.method == 'PUT':
        return handle_put_components()
    else:
        r = CustomResponse()
        r.set_status_code(404)
        response = jsonify(r.to_json())
        response.status_code = r.get_status_code()
        return response

bp_cat.register_blueprint(bp_comp)

@bp_prod.route('/', methods=['GET', 'POST', 'PUT'])
@check_authenticated(authentication_required=True)
def handle_productss():

    if request.method == 'GET':
        return handle_get_products()
    elif request.method == 'POST':
        return handle_post_products()
    elif request.method == 'PUT':
        return handle_put_products()
    else:
        r = CustomResponse()
        r.set_status_code(404)
        response = jsonify(r.to_json())
        response.status_code = r.get_status_code()
        return response

bp_cat.register_blueprint(bp_prod)

def handle_get_components():
    """
    GET api/v/catalogue/components/ Endpoint
    """

    # Clean Request
    component_ids = list(only_integers(request.args.getlist('component-id')))

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
        'item_id',
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


def handle_post_components():

    # Clean the Request
    custom_response = CustomResponse()

    component = collect_form_data(request)

    # Validate Request
    required_keys = ["component_type", "brand_id", "units", "Component_Names"]
    # brand_id is required, however it can be null.
    flag = False
    for key in required_keys:
        if key not in component.keys() or not component.get(key):
            if component.get('brand_id') == None:
                continue
            flag = True
            title = "Invalid Request."
            message = f"Missing {key} field."
            custom_response.insert_flash_message(
                    FlashMessage(
                        title=title,
                        message=message
                    )
                )

    if not flag:
        # Validate Component_Names Entry
        # [{"component_name": STRING, "primary_name": BOOL}]
        # There must be one and only one selected primary name
        try:
            component["Component_Names"] = json.loads(component["Component_Names"])
            primary_name = False
            primary_count = 0
            required_keys = ["component_name", "primary_name", "botanical_name", "name_id"]
            for name in component["Component_Names"]:
                if (not isinstance(name, dict)) or \
                    (set(name.keys()) != set(required_keys)):
                    flag = True
                    title = "Invalid Component Name Data."
                    message = "Component name settings are in the wrong format."
                    custom_response.insert_flash_message(
                        FlashMessage(
                            title=title,
                            message=message
                        )
                    )
                if name["component_name"] and \
                        not isinstance(name["component_name"], str):
                    flag = True
                    title = "Invalid Component Name."
                    message = "The component name must be a string of text."
                    custom_response.insert_flash_message(
                        FlashMessage(
                            title=title,
                            message=message
                        )
                    )
                if name["primary_name"] == 'true' or \
                        name["primary_name"] == 'True' or \
                        name["primary_name"] == True or \
                        name["primary_name"] == 1:
                    primary_name = True
                    primary_count += 1
                if "name_id" in name.keys():
                    name.pop("name_id")
            if not primary_name or primary_count != 1:
                flag = True
                title="Invalid Primary Name."
                message = "At least one and only one primary name must be selected."
                custom_response.insert_flash_message(
                    FlashMessage(
                        title=title,
                        message=message
                    )
                )
        except:
            flag = True

    if flag:
        custom_response.set_status_code(400)
        custom_response.insert_flash_message(
            FlashMessage(
                title="Proccessing Request Error.",
                message="There was an error proccessing the component name."
            )
        )
        response = jsonify(custom_response.to_json())
        response.status_code = 400
        return response

    # Post Components to Database
    custom_response = inv.post_component(
        custom_response,
        component
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response

def handle_put_components():

    # Clean the Request
    component = collect_form_data(request)

    # Get Components from Database
    custom_response = CustomResponse()

    custom_response = inv.put_component(
        custom_response,
        component
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response

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
        'manufacturing'
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

def handle_post_products():
    raise NotImplementedError

def handle_put_products():
    raise NotImplementedError
