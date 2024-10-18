'''
Handle Production Endpoints
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

bp = Blueprint('production', __name__, url_prefix='/production')

@bp.route('/lotnumbers', methods=['GET'])
@check_authenticated(authentication_required=True)
def handle_get_lot_and_batch_numbers():
    """
    GET api/production/lotnumbers Endpoint
    """

    # Clean Request
    lot_num_ids = list(only_integers(request.args.getlist('lot_num_id')))

    so_ids = list(only_integers(request.args.getlist('so_id')))

    so_detail_ids = list(only_integers(request.args.getlist('so_detail_id')))

    client_ids = list(only_integers(request.args.getlist('client_id')))

    product_ids = list(only_integers(request.args.getlist('product_id')))

    year_to_date = False
    yeartodate = request.args.get('year_to_date')
    if yeartodate == "true":
        year_to_date = True

    years = list(only_integers(request.args.getlist('year')))

    doc = False
    document = request.args.get('doc')
    if document == "true":
        doc = True

    desc = False
    desending = request.args.get('desc')
    if desending == "true":
        desc = True

    # Get Lot and Batch Numbers from the database
    custom_response = CustomResponse()
    custom_response = ord.get_lot_and_batch_numbers(
        custom_response,
        lot_num_ids,
        so_ids,
        so_detail_ids,
        client_ids,
        product_ids,
        desc,
        doc
    )

    response = jsonify(custom_response.to_json())
    response.status_code = custom_response.get_status_code()

    return response
