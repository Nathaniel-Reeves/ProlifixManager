'''
Handle all Inventory Functions
'''
import json
import mariadb
import os
import shutil
from datetime import (
    datetime,
    timezone
)
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
    error_message,
    Message
)
from redis import (
    Redis
)
from ..helper import (
    save_files,
    validate_float_in_dict,
    validate_int_in_dict
)

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

from .components import bp as components_bp
bp.register_blueprint(components_bp)


@bp.route('/checkin', methods=['POST', 'PUT'])
@check_authenticated(authentication_required=True)
def checkin():
    """
    """

    try:
        custom_response = CustomResponse()  # create a custom response object

        # Get Data
        form_data = dict(request.form)

        # Validate form data
        valid = True
        if not validate_float_in_dict(form_data, 'amount'):
            custom_response.insert_form_message(
                form_id=0,
                message=Message(
                    message="Invalid amount",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if not validate_int_in_dict(form_data, 'component_id'):
            custom_response.insert_form_message(
                form_id=1,
                message=Message(
                    message="Invalid component_id",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if not validate_int_in_dict(form_data, 'owner_id', equal_to=False):
            custom_response.insert_form_message(
                form_id=2,
                message=Message(
                    message="Invalid owner_id",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if not validate_int_in_dict(form_data, 'brand_id', equal_to=False):
            custom_response.insert_form_message(
                form_id=3,
                message=Message(
                    message="Invalid brand_id",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if request.method == 'POST':
            if "current_status" not in form_data.keys() or \
                form_data["current_status"] not in [
                'Ordered',
                'In Transit',
                'Received',
                'Found'
            ]:
                custom_response.insert_form_message(
                    form_id=4,
                    message=Message(
                        message="Invalid checkin status",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False

        if request.method == 'PUT':

            if not validate_int_in_dict(form_data, 'check_in_id', equal_to=False):
                custom_response.insert_form_message(
                    form_id=5,
                    message=Message(
                        message="Invalid check_in_id",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False

            if "current_status" not in form_data.keys() or \
                form_data["current_status"] not in [
                'Order Revised',
                'In Transit',
                'Received',
                'Received',
                'Missing Shipment',
                'Canceled',
                'Quarantined',
                'Released from Quarantine'
            ]:
                custom_response.insert_form_message(
                    form_id=6,
                    message=Message(
                        message="Invalid checkin status",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False

        if not valid:
            return jsonify(custom_response.to_json()), 400

        # Test DB Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )
        mariadb_connection.autocommit = False

        # Get Inventory Id, Create Inventory Id if None exists
        inv_id, custom_response = get_inventory_id(mariadb_connection,
                                                   request, custom_response)

        if not inv_id:
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500

        # Update Checkin Log
        check_in_id, custom_response = handle_check_in_log(mariadb_connection,
                                                           inv_id, request,
                                                           custom_response)

        if not check_in_id:
            print("Mariadb Rollback")
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500
        else:
            print("Mariadb Commit")
            mariadb_connection.commit()
            return jsonify(custom_response.to_json()), 200

    except Exception:
        if 'mariadb_connection' in locals():
            print("Mariadb Rollback")
            mariadb_connection.rollback()
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()

@bp.route('/checkout', methods=['POST', 'PUT'])
@check_authenticated(authentication_required=True)
def checkout():
    """
    """

    try:
        custom_response = CustomResponse()  # create a custom response object

        # Get Data
        form_data = dict(request.form)

        # Validate form data
        valid = True
        if not validate_float_in_dict(form_data, 'amount'):
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid amount",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if not validate_int_in_dict(form_data, 'component_id'):
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid component_id",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if not validate_int_in_dict(form_data, 'owner_id', equal_to=False):
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid owner_id",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if not validate_int_in_dict(form_data, 'brand_id', equal_to=False):
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid brand_id",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if request.method == 'POST':
            if "current_status" not in form_data.keys() or \
                form_data["current_status"] not in [
                'Wasted',
                'Lost',
                'Shipped',
                'Allocated',
                'Damaged',
                'Expired'
            ]:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="Invalid checkout status",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False

        if request.method == 'PUT':

            if not validate_int_in_dict(form_data, 'check_out_id', equal_to=False):
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="Invalid check_out_id",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False

            if "current_status" not in form_data.keys() or \
                form_data["current_status"] not in [
                'Used',
                'Batched',
                'Quarantined',
                'Released from Quarantine'
            ]:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="Invalid checkout status",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False

        if not valid:
            return jsonify(custom_response.to_json()), 400

        # Test DB Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )

        # Get Inventory Id, Create Inventory Id if None exists
        raise NotImplementedError
        inv_id = 0

        if not inv_id:
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500

        # Update Checkin Log
        check_out_id, custom_response = handle_check_in_log(mariadb_connection,
                                                            inv_id, request,
                                                            custom_response)

        if not check_out_id:
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500
        else:
            mariadb_connection.commit()
            return jsonify(custom_response.to_json()), 200

    except Exception:
        if 'mariadb_connection' in locals():
            mariadb_connection.rollback()
            mariadb_connection.close()
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()

def handle_check_in_log(mariadb_connection, inv_id, request, custom_response):

    try:
        cursor = mariadb_connection.cursor()
        form_data = dict(request.form)

        # Get Checkin Id, Create Checkin Id if None exists
        if request.method == 'PUT':

            # Validate Checkin Id
            base_query_1 = '''
                SELECT `check_in_id`
                FROM `Inventory`.`Check-in_Log`
                WHERE `check_in_id` = ?
                LIMIT 1
            '''
            cursor.execute(base_query_1, (form_data["check_in_id"],))
            result = cursor.fetchone()

            if not result:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="Invalid check_in_id",
                        message_type=MessageType.DANGER
                    )
                )
                return None, custom_response

            check_in_id = form_data["check_in_id"]

            updated_check_in_id, custom_response = update_check_in_log(
                mariadb_connection, check_in_id,
                inv_id, request, custom_response)
            if not updated_check_in_id:
                return None, custom_response
            else:
                return updated_check_in_id, custom_response

        else:
            # Create Checkin id
            base_query_2 = '''
                SELECT `check_in_id`
                FROM `Inventory`.`Check-in_Log`
                ORDER BY
                    `check_in_id` DESC
                LIMIT 1
            '''
            cursor.execute(base_query_2)
            result = cursor.fetchone()
            if not result:
                result = [0]
            check_in_id = result[0] + 1

            inserted_check_in_id, custom_response = insert_check_in_log(
                mariadb_connection, check_in_id,
                inv_id, request, custom_response)
            if not inserted_check_in_id:
                return None, custom_response
            else:
                return inserted_check_in_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def handle_check_out_log(mariadb_connection, inv_id, request, custom_response):
    raise NotImplementedError

def get_inventory_id(mariadb_connection, request, custom_response):
    try:
        form_data = dict(request.form)

        # Locate the component in the Inventory Table
        base_query_1 = """
            SELECT 
                a.`inv_id`,
                a.`item_id`
            FROM `Inventory`.`Inventory` a
            LEFT JOIN `Inventory`.`Components` b ON
                a.`item_id` = b.`component_id`
            WHERE b.`component_id` = ?
        """

        # Execute Query
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query_1, (form_data['component_id'],))
        result = cursor.fetchone()

        # If component not found in inventory table, create record
        if not result:
            inv_id, custom_response = post_component_to_inventory(
                mariadb_connection,
                request, custom_response
            )

        else:
            inv_id = result[0]

        return inv_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def post_component_to_inventory(mariadb_connection, request, custom_response):
    try:
        form_data = dict(request.form)

        # Build Insert Statement
        base_query = """
        INSERT INTO `Inventory`.`Inventory` (
            `item_id`,
            `actual_inventory`,
            `theoretical_inventory`,
            `recent_cycle_count_id`,
            `brand_id`,
            `owner_id`
        ) VALUES (
            ?, ?, ?, ?, ?, ?
        )
        """

        inputs = []
        inputs.append(form_data["component_id"])
        inputs.append(0)
        inputs.append(0)
        inputs.append(None)
        if "brand_id" in form_data.keys():
            inputs.append(form_data["brand_id"])
        else:
            inputs.append(None)
        if "owner_id" in form_data.keys():
            inputs.append(form_data["owner_id"])
        else:
            inputs.append(None)

        # Execute Statement
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))

        # Process Statement Return
        if cursor.lastrowid:
            inv_id = cursor.lastrowid
        else:
            inv_id = None
            custom_response.insert_flash_message(FlashMessage(
                message="Could not create inventory record.",
                message_type=MessageType.DANGER
            ))

        # Return New Inv_id
        return inv_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def get_component_type(mariadb_connection, request, custom_response):
    try:
        form_data = dict(request.form)

        # Build Insert Statement
        base_query = """
        SELECT
            `component_type`
        FROM 
            `Inventory`.`Components`
        WHERE
            `component_id` = ?
        LIMIT 1
        """

        inputs = []
        inputs.append(form_data["component_id"])

        # Execute Statement
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        component_type = cursor.fetchone()[0]

        # Return New Component_id
        return component_type, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def insert_check_in_log(mariadb_connection, check_in_id, inv_id, request, custom_response):
    try:
        cursor = mariadb_connection.cursor()
        form_data = dict(request.form)

        ### Save Files ###

        # Check Components Table and get the Component Type
        component_type, custom_response = get_component_type(
            mariadb_connection,
            request,
            custom_response)

        # If the Component does not exist in the components table,
        # Fail the checkin and report to the user.
        if not component_type:
            return None, custom_response

        file_objects = dict(request.files)

        if "doc" in form_data:
            doc = json.loads(form_data["doc"])
        else:
            doc = []

        # Create a location link for files related to this checkin
        location = \
            "components/" + \
            component_type + "/" + \
            "component_id-" + str(form_data["component_id"]) + "/" \
            "inventory_id-" + str(inv_id) + "/" \
            "check_in_id-" + str(check_in_id) + "/" + \
            "status-" + str(form_data["current_status"]) + \
            "  date-" + \
            str(datetime.utcnow().strftime("Y%Y-M%m-D%d H%H-M%M-S%S"))

        # Save Files
        doc, custom_response = save_files(
            doc, file_objects, custom_response, location)
        files_saved = True

        ### Create New Checkin Log ###

        # Build Insert Statement
        base_query_3 = '''
            INSERT INTO `Inventory`.`Check-in_Log` (
                `check_in_id`,
                `inv_id`,
                `supplier_item_id`,
                `lot_number`,
                `batch_number`,
                `amount`,
                `user_id`,
                `po_detail_id`,
                `current_status`,
                `current_status_notes`,
                `doc`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?
            )
        '''

        # Gather Inputs
        inputs = []
        inputs.append(check_in_id)
        inputs.append(inv_id)
        if 'component_id' in form_data.keys():
            inputs.append(form_data["component_id"])
        else:
            inputs.append(None)
        if 'lot_number' in form_data.keys():
            inputs.append(form_data["lot_number"])
        else:
            inputs.append(None)
        if 'batch_number' in form_data.keys():
            inputs.append(form_data["batch_number"])
        else:
            inputs.append(None)
        inputs.append(form_data["amount"])
        session_token = request.cookies.get('session')
        redis_connection = Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'])
        session_data = json.loads(redis_connection.get(session_token))
        inputs.append(session_data["user_id"])
        if 'po_detail_id' in form_data.keys():
            inputs.append(form_data["po_detail_id"])
        else:
            inputs.append(None)
        inputs.append(form_data["current_status"])
        if "current_status_notes" in form_data.keys():
            current_status_notes = form_data["current_status_notes"]
        else:
            current_status_notes = ""
        inputs.append(current_status_notes)
        inputs.append(json.dumps({
            "_id": check_in_id,
            "files": doc,
            "status_history": [
                {
                    "status": form_data["current_status"],
                    "date": datetime.now(timezone.utc).strftime(
                        "%d-%m-%y %H-%M-%S"
                    ),
                    "status_notes": current_status_notes,
                    "amount": form_data["amount"]
                }
            ]
        }))

        # Execute Statement
        cursor.execute(base_query_3, tuple(inputs))

        result = cursor.execute("SELECT `inv_id` FROM `Inventory`.`Inventory` WHERE `inv_id` =?;", (inv_id,))
        result = cursor.fetchone()

        if not result:
            # If insert statement fails, return error
            # and delete saved files.
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Failed to create new checkin log",
                    message_type=MessageType.DANGER
                )
            )

            # Delete Files
            print("Deleting Files")
            shutil.rmtree(
                os.path.join(
                    app.config['UPLOAD_FOLDER'], location
                )
            )

            return None, custom_response

        ### Update Inventory Table ###
        inv_changed = False
        if form_data["current_status"] in [
            "Ordered",
            "In Transit"
        ]:
            inv_changed, custom_response = add_theoretic_inventory(mariadb_connection, inv_id, request, custom_response)

        if form_data["current_status"] in [
                "Received",
                "Found"
        ]:
            inv_changed, custom_response = add_actual_inventory(mariadb_connection, inv_id, request, form_data)

        if form_data["current_status"] in [
                "Received", 
                "Found", 
                "Ordered",
                "In Transit"
            ] and not inv_changed:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Could not update inventory record.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response

        return check_in_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        if "files_saved" in locals():
            # Delete Files
            print("Deleting Files")
            shutil.rmtree(
                os.path.join(
                    app.config['UPLOAD_FOLDER'], location
                )
            )
        return None, custom_response

def update_check_in_log(mariadb_connection, check_in_id, inv_id, request, custom_response):
    try:

        cursor = mariadb_connection.cursor()
        form_data = dict(request.form)

        # Check Components Table and get the Component Type
        component_type, custom_response = get_component_type(
            mariadb_connection,
            request,
            custom_response
        )

        # If the Component does not exist in the components table,
        # Fail the checkin and report to the user.
        if not component_type:
            return None, custom_response

        # Find most recent/previous checkin status
        base_query = '''
            SELECT
                `check_in_id`,
                `current_status`
            FROM
                `Inventory`.`Check-in_Log`
            WHERE
                `check_in_id` = ?
            LIMIT 1
        '''

        cursor.execute(base_query, (check_in_id,))
        result = cursor.fetchone()
        if result:
            previous_status = result[1]
        else:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Failed to find previous status.",
                    message_detail="Previous status not found. Talk to IT Support.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response
        current_status = form_data["current_status"]

        ### Compare Previous and Current Status ###
        invalid_status_update_message = FlashMessage(
            message="Checkin status did not change.",
            message_detail="Previous status: '" + previous_status +
            "', Current status: '" + current_status + "' is an invalid status update.",
            message_type=MessageType.DANGER
        )

        if previous_status == "Ordered":
            if current_status not in [
                "Received",
                "Missing Shipment",
                "Canceled",
                "Quarantined",
                "In Transit",
                "Revised Order Decreased",
                "Revised Order Increased"
            ]:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response
            if current_status in [
                "Received",
                "Missing Shipment",
                "Canceled",
                "Quarantined",
                "Revised Order Decreased"
            ]:
                inv_changed, custom_response = remove_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            if current_status == "Revised Order Increased":
                inv_changed, custom_response = add_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)

        elif previous_status == "Revised":
            if current_status not in [
                "Received",
                "Missing Shipment",
                "Canceled",
                "Quarantined",
                "In Transit"
            ]:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response
            if current_status in [
                "Received",
                "Missing Shipment",
                "Canceled",
                "Quarantined"
            ]:
                inv_changed, custom_response = remove_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)

        elif previous_status == "In Transit":
            if current_status not in [
                "Received",
                "Missing Shipment",
                "Canceled",
                "Quarantined"
            ]:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response
            if current_status in [
                "Received",
                "Missing Shipment",
                "Canceled",
                "Quarantined"
            ]:
                inv_changed, custom_response = remove_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)

        elif previous_status == "Received":
            if current_status == "Quarantined":
                inv_changed, custom_response = remove_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            elif current_status == "Received":
                inv_changed, custom_response = remove_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            else:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response

        elif previous_status == "Missing Shipment":
            if current_status not in [
                "Received",
                "Canceled",
                "Quarantined"
            ]:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)

        elif previous_status == "Found":
            if current_status == "Quarantined":
                inv_changed, custom_response = remove_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            elif current_status == "Found":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            else:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response

        elif previous_status == "Quarantined":
            if current_status == "Released from Quarantine":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            elif current_status == "Quarantined":
                inv_changed, custom_response = remove_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            else:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response

        elif previous_status == "Released from Quarantine":
            if current_status == "Released from Quarantine":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            elif current_status == "Quarantined":
                inv_changed, custom_response = remove_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            else:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response

        else:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid Previous Checkin Status",
                    message_detail="Previous status: '" + previous_status +
                    "'is invalid. Contact IT Support to fix this issue.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response

        if not inv_changed:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="No inventory changes were made.",
                    message_detail="Updates to Inventory Failed. Contact IT Support to fix this issue.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response

        # Get current doc from checkin log
        base_query_2 = '''
            SELECT
                `doc`
            FROM 
                `Inventory`.`Check-in_Log`
            WHERE
                `check_in_id` = ?
            LIMIT 1
        '''

        cursor.execute(base_query_2, (check_in_id, ))
        result = cursor.fetchone()
        if result:
            current_doc = json.loads(result[0])
        else:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Failed to find current doc.",
                    message_detail="Current doc not found. Talk to IT Support.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response

        # Save Files
        file_objects = dict(request.files)

        if "doc" in form_data:
            doc = json.loads(form_data["doc"])
        else:
            doc = []

        # Create a location link for files related to this checkin
        location = \
            "components/" + \
            component_type + "/" + \
            "component_id-" + str(form_data["component_id"]) + "/" \
            "inventory_id-" + str(inv_id) + "/" \
            "check_in_id-" + str(check_in_id) + "/" + \
            "status-" + str(form_data["current_status"]) + \
            "  date-" + str(datetime.utcnow().strftime("Y%Y-M%m-D%d H%H-M%M-S%S"))

        # Save Files
        doc, custom_response = save_files(
            doc, file_objects, custom_response, location)

        # Create new doc data
        new_doc_files = current_doc["files"] + doc
        if "current_status_notes" in form_data.keys():
            current_status_notes = form_data["current_status_notes"]
        else:
            current_status_notes = ""
        current_doc["status_history"].append({
            "status": form_data["current_status"],
            "date": datetime.now(timezone.utc).strftime(
                "%d-%m-%y %H-%M-%S"
            ),
            "status_notes": current_status_notes,
            "amount": form_data["amount"]
        })
        new_doc = current_doc.copy()
        new_doc["files"] = new_doc_files

        ### Update Checkin Log ###

        # Build Update Statement
        base_query_3 = '''
            UPDATE `Inventory`.`Check-in_Log`
            SET
                `current_status` = ?,
                `current_status_notes` = ?,
                `doc` = ?
            WHERE
                `check_in_id` = ?
        '''

        # Gather Inputs
        inputs = []
        inputs.append(current_status)
        if "current_status_notes" in form_data.keys():
            inputs.append(form_data["current_status_notes"])
        else:
            inputs.append("")
        inputs.append(json.dumps(new_doc))
        inputs.append(check_in_id)

        # Execute Statement
        cursor.execute(base_query_3, tuple(inputs))

        if not result:
            # If insert statement fails, return error
            # and delete saved files.
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Failed to create new checkin log",
                    message_type=MessageType.DANGER
                )
            )
            error = error_message()
            custom_response.insert_flash_message(error)

            # Delete Files
            shutil.rmtree(
                os.path.join(
                    app.config['UPLOAD_FOLDER'], location
                )
            )

            return None, custom_response
        else:
            return check_in_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def insert_check_out_log(mariadb_connection, check_out_id, request, custom_response):
    raise NotImplementedError

def add_actual_inventory(mariadb_connection, inv_id, request, custom_response):
    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `actual_inventory` = `actual_inventory` + ?
            WHERE
                `inv_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["amount"]))
        inputs.append(inv_id)
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        message = FlashMessage(
            message="Failed to update inventory",
            message_type=MessageType.DANGER
        )
        custom_response.insert_flash_message(message)
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def remove_actual_inventory(mariadb_connection, inv_id, request, custom_response):
    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `actual_inventory` = `actual_inventory` - ?
            WHERE
                `inv_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["amount"]))
        inputs.append(inv_id)
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        message = FlashMessage(
            message="Failed to update inventory",
            message_type=MessageType.DANGER
        )
        custom_response.insert_flash_message(message)
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def add_theoretic_inventory(mariadb_connection, inv_id, request, custom_response):
    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `theoretical_inventory` = `theoretical_inventory` + ?
            WHERE
                `inv_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["amount"]))
        inputs.append(inv_id)
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        message = FlashMessage(
            message="Failed to update inventory",
            message_type=MessageType.DANGER
        )
        custom_response.insert_flash_message(message)
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def remove_theoretic_inventory(mariadb_connection, inv_id, request, custom_response):
    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `theoretical_inventory` = `theoretical_inventory` - ?
            WHERE
                `inv_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["amount"]))
        inputs.append(inv_id)
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        message = FlashMessage(
            message="Failed to update inventory",
            message_type=MessageType.DANGER
        )
        custom_response.insert_flash_message(message)
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response
