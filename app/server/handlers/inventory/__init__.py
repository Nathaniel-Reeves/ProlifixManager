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


@bp.route('/checkin', methods=['POST', 'GET'])
@check_authenticated(authentication_required=True)
def checkin():
    """
    """
    try:

        custom_response = CustomResponse()

        print("This Works")
        message = FlashMessage(
            message="This Works!",
            message_type=MessageType.INFO
        )
        custom_response.insert_flash_message(message)
        return jsonify(custom_response.to_json())
    except Exception:
        error = error_message()
        return jsonify(custom_response.insert_flash_message(error).to_json())
