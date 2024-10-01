'''
Handle Orders Data
'''
from sqlalchemy import select
from sqlalchemy.orm import defer

from view.response import CustomResponse
import model as db
from .execute import execute_query

from model import organizations as org

import datetime

def get_sales_orders(
        custom_response,
        so_ids,
        client_ids,
        year_to_date,
        year,
        populate,
        doc
    ):

    # build the query
    stm = select(db.Sales_Orders)

    if not doc:
        stm = stm.options(defer(db.Sales_Orders.doc))

    if so_ids:
        stm = stm.where(db.Sales_Orders.so_id.in_(so_ids))

    if client_ids:
        stm = stm.where(db.Sales_Orders.client_id.in_(client_ids))

    if year_to_date:
        today = datetime.datetime.now()
        year_ago = today - datetime.timedelta(days=365)
        stm = stm.where(db.Sales_Orders.order_date >= year_ago)

    if year:
        stm = stm.where(db.Sales_Orders.order_date >= datetime.datetime(year, 1, 1))
        stm = stm.where(db.Sales_Orders.order_date < datetime.datetime(year + 1, 1, 1))

    # execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        sales_order = row[0].to_dict()

        sales_orders_payments = {'sales_orders_payments': []}
        sale_order_detail = {'sale_order_detail': []}
        client = {'client': []}


        if 'sales_orders_payments' in populate:
            r = CustomResponse()
            resp = get_sales_orders_payments(r, [pk], [], False)
            sales_orders_payments = {'sales_orders_payments':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'sale_order_detail' in populate:
            r = CustomResponse()
            resp = get_sale_order_detail(r, [], [pk], False)
            sale_order_detail = {'sale_order_detail':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'client' in populate:
            r = CustomResponse()
            resp = org.get_organization_names(r, [], [sales_order['client_id']], True)
            client = {'client':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({ **sales_order, **sales_orders_payments, **sale_order_detail, **client })

    return custom_response

def get_sales_orders_payments():
    raise NotImplementedError

def get_sale_order_detail():
    raise NotImplementedError

def get_purchase_orders():
    raise NotImplementedError

def get_purchase_order_detail():
    raise NotImplementedError