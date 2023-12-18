'''
Handle Inventory Data
'''
import json
from sqlalchemy import select, text

from view.response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
import model as db
from model.connector import get_session
from .package import package_data

def get_components(custom_response):
    return custom_response