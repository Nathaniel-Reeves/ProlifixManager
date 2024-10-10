'''
Handle Orders Data
'''
from sqlalchemy import select
from sqlalchemy.orm import defer

from view.response import CustomResponse
import model as db
from .execute import execute_query

from model import organizations as org

from .products import get_products, get_product_variants, get_formulas
from controller import organizations as org_controller

import datetime

def get_sales_orders(
        custom_response,
        so_ids,
        client_ids,
        year_to_date,
        years,
        populate,
        doc
    ):

    # build the query
    stm = select(db.Sales_Orders)
    exclude = []

    if not doc:
        exclude.append('doc')

    if so_ids:
        stm = stm.where(db.Sales_Orders.so_id.in_(so_ids))

    if client_ids:
        stm = stm.where(db.Sales_Orders.client_id.in_(client_ids))

    if year_to_date:
        today = datetime.datetime.now()
        year_ago = today - datetime.timedelta(days=365)
        stm = stm.where(db.Sales_Orders.order_date >= year_ago)

    if years:
        stm = stm.where(db.Sales_Orders.year.in_(years))

    stm = stm.order_by(db.Sales_Orders.so_id.desc())

    # execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        sales_order = row[0].to_dict(exclude=exclude)

        sales_orders_payments = {'sales_orders_payments': []}
        sale_order_detail = {'sale_order_detail': []}
        client = {'client': []}


        if 'sales_orders_payments' in populate:
            r = CustomResponse()
            resp = get_sales_orders_payments(r, [], [pk], [], False)
            sales_orders_payments = {'sales_orders_payments':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'sale_order_detail' in populate:
            r = CustomResponse()
            resp = get_sale_order_detail(r, [], [pk], [], [], [], ['product','variant','formula'], False)
            sale_order_detail = {'sale_order_detail':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'client' in populate:
            r = CustomResponse()
            resp = org_controller.get_organization_names(r, [], [sales_order['organization_id']], True)
            client = {'client':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({ **sales_order, **sales_orders_payments, **sale_order_detail, **client })

    return custom_response

def get_sales_orders_payments(
        custom_response,
        payment_ids,
        so_ids,
        populate,
        doc
    ):

    # build the query
    stm = select(db.Sales_Orders_Payments)
    exclude = []

    if not doc:
        exclude.append('doc')

    if payment_ids:
        stm = stm.where(db.Sales_Orders_Payments.payment_id.in_(payment_ids))

    if so_ids:
        stm = stm.where(db.Sales_Orders_Payments.so_id.in_(so_ids))

    # execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        sales_order_payment = row[0].to_dict(exclude=exclude)

        sales_order = {'sales_order': []}

        if 'sales_order' in populate:
            r = CustomResponse()
            resp = get_sales_orders(r, [sales_order_payment['so_id']], [], False, [], [], False)
            sales_order = {'sales_order':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({ **sales_order_payment, **sales_order })

    return custom_response

def get_sale_order_detail(
        custom_response,
        so_detail_ids,
        so_ids,
        product_ids,
        variant_ids,
        formula_ids,
        populate,
        doc
    ):

    # build the query
    stm = select(db.Sale_Order_Detail)
    exclude = []

    if not doc:
        exclude.append('doc')

    if so_detail_ids:
        stm = stm.where(db.Sale_Order_Detail.so_detail_id.in_(so_detail_ids))

    if so_ids:
        stm = stm.where(db.Sale_Order_Detail.so_id.in_(so_ids))

    if product_ids:
        stm = stm.where(db.Sale_Order_Detail.product_id.in_(product_ids))

    if variant_ids:
        stm = stm.where(db.Sale_Order_Detail.variant_id.in_(variant_ids))

    if formula_ids:
        stm = stm.where(db.Sale_Order_Detail.formula_id.in_(formula_ids))

    # execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        sale_order_detail = row[0].to_dict(exclude=exclude)

        sale_order = {'sale_order': []}
        product = {'product': []}
        variant = {'variant': []}
        formula = {'formula': []}

        if 'sale_order' in populate:
            r = CustomResponse()
            resp = get_sales_orders(r, [sale_order_detail['so_id']], [], False, [], [], False)
            sale_order = {'sale_order':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'product' in populate:
            r = CustomResponse()
            resp = get_products(r, [sale_order_detail['product_id']], [], [], [], False)
            product = {'product':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'variant' in populate:
            r = CustomResponse()
            resp = get_product_variants( r, [sale_order_detail['variant_id']], [], False)
            variant = {'variant':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'formula' in populate:
            r = CustomResponse()
            resp = get_formulas( r, [sale_order_detail['formula_id']], [], [], doc)
            formula = {'formula':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({ **sale_order_detail, **sale_order, **product, **variant, **formula })

    return custom_response

def get_purchase_orders():
    raise NotImplementedError

def get_purchase_order_detail():
    raise NotImplementedError