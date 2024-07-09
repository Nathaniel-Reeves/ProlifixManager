'''
Handle Orders Data
'''
from sqlalchemy import select

from view.response import CustomResponse
import model as db
from .execute import execute_query

def get_sales_orders():
    raise NotImplementedError

def get_purchase_orders():
    raise NotImplementedError

def get_purchase_order_detail():
    raise NotImplementedError