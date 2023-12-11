'''
Handle Component Functions
'''
import json
from datetime import (
    datetime,
    timezone
)
import mariadb
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app as app
)
from redis import (
    Redis
)

from view.auth import check_authenticated
from view.response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message,
    Message
)
from view.helper import (
    save_files,
    delete_directory,
    validate_float_in_dict,
    validate_int_in_dict,
    only_integers
)

bp = Blueprint('products', __name__, url_prefix='/products')
