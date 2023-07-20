'''
Handle Component Functions
'''
import json
import mariadb
import os
import datetime
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
    save_files
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

        # Test DB Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )

        # Get Data
        form_data = dict(request.form)

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
            inv_id, custom_response = post_component_to_inventory(mariadb_connection,
                form_data, custom_response)
        else:
            inv_id = result[0]

        if not inv_id:
            return jsonify(custom_response.to_json()), 500

        # Create checkin entry in log

        # Get File Data
        form_data = dict(request.form)
        file_objects = dict(request.files)
        if "doc" in form_data:
            doc = json.loads(form_data["doc"])
        else:
            doc = []

        location = os.path.join(
            "components/",
            result[2],
            "component_id-" + str(form_data["component_id"]),
            "inventory_id-" + str(inv_id),
            "checkin_docs-" + str(
                datetime.datetime.utcnow()
            )
        )

        # Save Files
        doc, custom_response = save_files(
            doc, file_objects, custom_response, location)

        # Create Checkin Log
        base_query_2 = """
            INSERT INTO `Inventory`.`Check-in_Log` (
                `inv_id`,
                `amount`,
                `user_id`,
                `po_detail_id`,
                `current_status`
            ) VALUES (
              ?, ?, ?, ?, ?
            )
        """

        # Execute Statement
        inputs_1 = []
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

        # Execute Statement
        cursor.execute(base_query_1, tuple(inputs_1))
        result = cursor.fetchone()

        check_in_id = result[0]

        if not check_in_id:
            checkin_insert_fail = FlashMessage(
                message="Failed to insert record in Checkin Log.",
                message_type=MessageType.DANGER
            )
            custom_response.insert_flash_message(checkin_insert_fail)
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500

        # Update checkin record with documents
        if doc:
            base_query_3 = '''
            UPDATE 
                JSON_SET()
            '''

        # Update Inventory
        # update_inventory(mariadb_connection, form_data, custom_response)
        message = FlashMessage(
            message="Worked",
            message_type=MessageType.INFO
        )
        custom_response.insert_flash_message(message)
        mariadb_connection.commit()
        return jsonify(custom_response.to_json()), 200
    
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500


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
