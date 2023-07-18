'''
Handle all Inventory Functions
'''
from flask import (
    Blueprint,
)

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

from .components import bp as components_bp
bp.register_blueprint(components_bp)
