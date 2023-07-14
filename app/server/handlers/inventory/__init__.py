"""
Handles all inventory functions
"""
from flask import (
    Blueprint
)

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

from .components import bp as components_bp
inventory_bp.register_blueprint(components_bp)
