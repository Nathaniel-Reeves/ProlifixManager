'''
Handle Component Functions
'''
import json
import mariadb
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
    error_message
)
from redis import (
    Redis
)
from ..helper import (
    only_integers,
    save_files,
    validate_float_in_dict,
    validate_int_in_dict
)

bp = Blueprint('components', __name__, url_prefix='/components')

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def get_components():
    '''
    Get all Components
    '''
    try:
        custom_response = CustomResponse()  # Create an instance of CustomResponse

        # Test DB Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )

        # Build Query
        docs = request.args.get("docs", type=bool, default=False)
        if not docs:
            base_query = '''
            SELECT
                JSON_OBJECT(
                    'component_id', a.`component_id`,
                    'component_type', a.`component_type`,
                    'date_entered', a.`date_entered`,
                    'owner_id', a.`owner_id`,
                    'component_name', b.`component_name`
                )
            AS component_objects
            FROM `Inventory`.`Components` a
            LEFT JOIN `Inventory`.`Component_Names` b ON
                a.`component_id` = b.`component_id`
            WHERE b.`primary_name` = true
            '''
        else:
            base_query = '''
            SELECT
                JSON_OBJECT(
                    'component_id', a.`component_id`,
                    'component_type', a.`component_type`,
                    'date_entered', a.`date_entered`,
                    'owner_id', a.`owner_id`,
                    'doc', a.`doc`,
                    'component_name', b.`component_name`
                )
            AS component_objects
            FROM `Inventory`.`Components` a
            LEFT JOIN `Inventory`.`Component_Names` b ON
                a.`component_id` = b.`component_id`
            WHERE b.`primary_name` = true
            '''

        verbose = request.args.get("verbose", type=bool, default=False)

        inputs = []

        org_ids = request.args.getlist('org-id')
        if org_ids:
            cleaned_org_ids = list(only_integers(org_ids))
            base_query += f''' AND a.`owner_id` IN ({", ".join(["?"] * len(cleaned_org_ids))})'''
            inputs += cleaned_org_ids

        component_ids = request.args.getlist('component-id')
        if component_ids:
            cleaned_component_ids = list(only_integers(component_ids))
            base_query += f''' AND a.`component_id` IN ({", ".join(["?"] * len(cleaned_component_ids))})'''
            inputs += cleaned_component_ids

        component_types = request.args.getlist('component-type')
        if component_types:
            base_query += f''' AND a.`component_type` IN ({", ".join(["?"] * len(component_types))})'''
            inputs += component_types

        # Execute Query
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        result = cursor.fetchall()

        # Process Components
        populate = request.args.getlist('populate')
        components = {}
        for row in result:
            json_row = json.loads(row[0])
            component_id = json_row['component_id']
            components[component_id] = json_row

            # Populate child resources
            if 'names' in populate:
                components, custom_response = populate_component_names(
                                                cursor, component_id, 
                                                components, custom_response, 
                                                verbose)

        # Insert the processed component data into the response
        custom_response.insert_data(components)
        if not components:
            return jsonify(custom_response.to_json()), 404
        return jsonify(custom_response.to_json()), 200

    except Exception as error:
        custom_response.insert_flash_message(
            FlashMessage(
                message=str(error),
                message_type=MessageType.DANGER
            )
        )
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()

def populate_component_names(cursor, component_id,
                             components, custom_response,
                             verbose):
    """
    Populates Component Objects with their
    alias names.

    Attributes:
        cursor (MaraDB.cursor): Database cursor
        component_id (int): Component Id
        components (dict): Dictionary of Component Objects
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose Flag

    Returns:
        names (list of dicts): List of alias name dicts

    Raises:
        Error: FlashMessage Error
    """

    try:

        # Build Query
        base_query = '''
        SELECT
            JSON_OBJECT(
                'name_id', a.`name_id`,
                'component_name', a.`component_name`,
                'primary_name', a.`primary_name`
            )
        AS component_name_objects
        FROM `Inventory`.`Component_Names` a
        WHERE a.`component_id` = ?
        '''

        # Execute Query
        cursor.execute(base_query, (component_id,))
        results = cursor.fetchall()

        # Process Data
        names = []
        for row in results:
            names.append(json.loads(row[0]))

        components[component_id]['names'] = names
        if not names and verbose:
            not_found = FlashMessage(
                message=f'No names found for component (ID: {component_id}).'
            )
            return components, custom_response.insert_flash_message(not_found)
        return components, custom_response

    except Exception:
        error=error_message()
        return components, custom_response.insert_flash_message(error)

@bp.route('/checkin', methods=['POST'])
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

        if not validate_int_in_dict(form_data, 'check_in_id', equal_to=False):
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid check_in_id",
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

        if "current_status" not in form_data.keys() or \
        form_data["current_status"] not in [
            'Ordered',
            'In Transit',
            'Received',
            'Released from Q',
            'Found'
        ]:
            custom_response.insert_flash_message(
                FlashMessage(
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

        # Update Checkin Log
        status, custom_response = update_checkin_log(mariadb_connection,
                                                     form_data, custom_response)

        # Update Inventory Records
        status, custom_response = update_inventory(mariadb_connection,
                         form_data, custom_response)

        if not status:
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

@bp.route('/checkout', methods=['POST'])
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

        if not validate_int_in_dict(form_data, 'check_in_id', equal_to=False):
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid check_in_id",
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

        if "current_status" not in form_data.keys() or \
            form_data["current_status"] not in [
            'Ordered',
            'In Transit',
            'Received',
            'Released from Quarantine',
            'Found'
        ]:
            custom_response.insert_flash_message(
                FlashMessage(
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

        # Update Checkin Log
        status, inv_id, custom_response = update_checkin_log(mariadb_connection,
                                                     form_data, custom_response)

        # Update Inventory Records
        status, custom_response = update_inventory(mariadb_connection,
                                                   form_data, custom_response)


        if not status:
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

def update_checkin_log(mariadb_connection, form_data, custom_response):
    # Update Check in Log Records

    component_type, custom_response = get_component_type(
        mariadb_connection,
        form_data, custom_response
        )

     # Create checkin entry in log

     # Get File Data
        if "doc" in form_data:
            doc = json.loads(form_data["doc"])
        else:
            doc = []

        location = \
            "components/" + \
            component_type + "/" + \
            "component_id-" + str(form_data["component_id"]) + "/" \
            "inventory_id-" + str(inv_id) + "/" \
            "check_in_id-" + str(check_in_id) + "/"

        # Save Files
        doc, custom_response = save_files(
            doc, file_objects, custom_response, location)

        # Create Checkin Log
        base_query_2b = """
            INSERT INTO `Inventory`.`Check-in_Log` (
                `check_in_id`,
                `inv_id`,
                `amount`,
                `user_id`,
                `po_detail_id`,
                `current_status`,
                `doc`
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?
            )
        """

        # Build Query
        inputs_1 = []

        base_query_2a = '''
            SELECT `check_in_id`
            FROM `Inventory`.`Check-in_Log`
            ORDER BY
                `check_in_id` DESC
            LIMIT 1
        '''
        cursor.execute(base_query_2a)
        result = cursor.fetchone()
        if not result:
            result = [0]
        check_in_id = result[0] + 1
        inputs_1.append(check_in_id)

        inputs_1.append(inv_id)

        inputs_1.append(form_data["amount"])

        session_token = request.cookies.get('session')
        redis_connection = Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'])
        session_data = json.loads(redis_connection.get(session_token))
        inputs_1.append(session_data["user_id"])

        if form_data["po_detail_id"]:
            inputs_1.append(form_data["po_detail_id"])
        else:
            inputs_1.append(None)

        inputs_1.append(form_data["current_status"])

        inputs_1.append(json.dumps({
            "_id": check_in_id,
            "files": doc,
            "status_history": [
                {
                    "status": form_data["current_status"],
                    "date": datetime.now(timezone.utc).strftime(
                        "%d-%m-%y %H-%M-%S"
                    )
                }
            ]
        }))

        # Execute Statement
        cursor.execute(base_query_2b, tuple(inputs_1))

def update_inventory(mariadb_connection, form_data, custom_response):
    try:

        # Locate the component in the Inventory Table
        base_query_1 = """
            SELECT 
                a.`inv_id`,
                a.`item_id`,
                b.`component_type`
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
                form_data, custom_response
            )
            component_type, custom_response = get_component_type(
                mariadb_connection,
                form_data, custom_response
            )
        else:
            update_inventory(mariadb_connection,
                             form_data, custom_response)
            inv_id = result[0]
            component_type = result[2]

        if not inv_id or not component_type:
            return inv_id, custom_response

        # Get most recent checkin log status update
        base_query_1 = '''
            SELECT 
                `check_in_id`,
                `current_status`,
                `doc`
            FROM `Inventory`.`Check-in_Log`
            WHERE
                `inv_id` = ?
            ORDER BY 
                `check_in_id` DESC 
            LIMIT 1
        '''

        # Build Query
        # match form_data["current_status"]:
            

def get_component_type(mariadb_connection, form_data, custom_response):
    try:

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

def post_component_to_inventory(mariadb_connection, form_data, custom_response):
    try:

        # Build Insert Statement
        base_query = """
        INSERT INTO `Inventory`.`Inventory` (
            `item_id`,
            `actual_inventory`,
            `theoretical_inventory`,
            `recent_cycle_count_id`,
            `brand_id`
        ) VALUES (
            ?, ?, ?, ?, ?
        )
        """

        inputs = []
        inputs.append(form_data["component_id"])
        match form_data["current_status"]:
            case "Ordered":
                inputs.append(0)
                inputs.append(form_data["amount"])
            case "In Transit":
                inputs.append(0)
                inputs.append(form_data["amount"])
            case "Received":
                inputs.append(form_data["amount"])
                inputs.append(0)
            case "Released from Q":
                inputs.append(form_data["amount"])
                inputs.append(0)
            case "Found":
                inputs.append(form_data["amount"])
                inputs.append(0)
            case _:
                inputs.append(0)
                inputs.append(0)

        inputs.append(None)
        inputs.append(None)

        # Execute Statement
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))

        # Process Statement Return
        if cursor.lastrowid:
            inv_id = cursor.lastrowid
            mariadb_connection.commit()
        else:
            inv_id = None
            custom_response.insert_flash_message(FlashMessage(
                message="Could not create inventory record.",
                message_type=MessageType.DANGER
            ))
            mariadb_connection.rollback()

        # Return New Inv_id
        return inv_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response
