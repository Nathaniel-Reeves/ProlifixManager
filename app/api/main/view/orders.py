'''
Handle Orders Endpoints
'''
import json
from flask import (
    Blueprint,
    request,
    jsonify
)
from controller import orders as ord
from .auth import check_authenticated
from .helper import only_integers, check_type, str_to_int
from .response import CustomResponse

import datetime

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/sales', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_sales():
    """
    GET api/orders/sales Endpoint
    """

    # Clean Request
    so_ids = list(only_integers(request.args.getlist('so_id')))

    client_ids = list(only_integers(request.args.getlist('client_id')))

    year_to_date = False
    yeartodate = request.args.get('year_to_date')
    if yeartodate == "true":
        year_to_date = True

    years = list(only_integers(request.args.getlist('year')))

    populate_request = request.args.getlist('populate')
    valid_populate = [
        'sales_orders_payments',
        'sale_order_detail',
        'client',
        'lot_and_batch_numbers'
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

    # Get Sales Orders from the database
    custom_response = CustomResponse()
    custom_response = ord.get_sales_orders(
        custom_response,
        so_ids,
        client_ids,
        year_to_date,
        years,
        populate,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response