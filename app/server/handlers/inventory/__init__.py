'''
Handle all Inventory Functions
'''
import json
import mariadb
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app as app
)
from ..auth import check_authenticated
from ..response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
bp = Blueprint('inventory', __name__, url_prefix='/inventory')

from .components import bp as components_bp
bp.register_blueprint(components_bp)
