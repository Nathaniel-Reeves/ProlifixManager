'''
Handle all Inventory Functions
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

from ..auth import check_authenticated
from ..response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message,
    Message
)
from ..helper import (
    save_files,
    delete_directory,
    validate_float_in_dict,
    validate_int_in_dict,
    only_integers
)

bp = Blueprint('inventory', __name__, url_prefix='/inventory')

from .components import bp as components_bp
bp.register_blueprint(components_bp)

from .products import bp as products_bp
bp.register_blueprint(products_bp)

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def fetch_inventory():
    """
    Fetch Inventory from Database.
    Populate and filter items as requested.
    """

    try:
        custom_response = CustomResponse()

        # Test Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )

        # Build Query
        base_query = '''
            SELECT
                JSON_OBJECT(
                    'inv_id', a.`inv_id`, 
                    'item_id', a.`item_id`,
                    'owner_id', a.`owner_id`,
                    'is_component', a.`is_component`,
                    'is_product', a.`is_product`,
                    'actual_inventory', a.`actual_inventory`,
                    'theoretical_inventory', a.`theoretical_inventory`,
                    'units', CASE WHEN a.`is_component` THEN c.`units` ELSE 'units' END,
                    'recent_cycle_count_id', a.`recent_cycle_count_id`,
                    'item_name', CASE WHEN a.`is_component` THEN d.`component_name` ELSE e.`product_name` END,
                    'item_type', CASE WHEN a.`is_component` THEN c.`component_type` ELSE 'product' END,
                    'component_id', b.`component_id`,
                    'product_id', b.`product_id`
                )
            AS item_objects
            FROM `Inventory`.`Inventory` a
            JOIN `Inventory`.`Item_id` b ON
                a.`item_id` = b.`item_id`
            LEFT JOIN `Inventory`.`Components` c ON
                b.`component_id` = c.`component_id`
            LEFT JOIN `Inventory`.`Component_Names` d ON 
                b.`component_id` = d.`component_id` AND
                d.`primary_name` = true
            LEFT JOIN `Products`.`Product_Master` e ON
                b.`product_id` = e.`product_id`
        '''

        owner_id = request.args.getlist('owner-id')
        item_types = request.args.getlist('item-type')
        inputs = []
        if owner_id or (item_types and 'all' not in item_types):
            base_query += "WHERE "

            if owner_id:
                cleaned_owner_id = list(only_integers(owner_id))
                base_query += f'''a.`owner_id` IN ({", ".join(["?"] * len(cleaned_owner_id))})'''
                inputs += cleaned_owner_id

            # Insert Item Type Filters
            type_filter = []
            valid_component_types = ['powder','liquid','container','pouch','shrink_band','lid','label','capsule','misc','scoop','desiccant','box','carton','packaging_material']
            product_filter = False
            component_filter = False

            for item_type in item_types:
                if item_type in valid_component_types:
                    type_filter.append(item_type)
                    component_filter = True
                    continue
                if item_type == "product":
                    product_filter = True

            if component_filter:
                if owner_id:
                    base_query += " AND "
                base_query += f''' c.`component_type` IN ({", ".join(["?"] * len(type_filter))})'''
                inputs += type_filter

            if not product_filter:
                if owner_id or component_filter:
                    base_query += " AND "
                base_query += f'''a.`is_component` = true '''
            else:
                if owner_id or component_filter:
                    base_query += " OR "
                base_query += f'''a.`is_product` = true '''

        verbose = request.args.get("verbose", type=bool, default=False)

        populate = request.args.getlist('populate')

        # Execute Query
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        result = cursor.fetchall()

        if not result:
            custom_response.insert_flash_message(FlashMessage(
                message='No inventory found',
                message_type=MessageType.WARNING))
            return jsonify(custom_response.to_json()), 404

        # Process inventory
        inventory = {}
        for row in result:
            json_row = json.loads(row[0])
            item_id = json_row['item_id']
            inv_id = json_row['inv_id']
            recent_cycle_count_id = json_row['recent_cycle_count_id']
            owner_id = json_row['owner_id']
            component_id = json_row['component_id']
            product_id = json_row['product_id']

            # Populate child resources
            if 'checkins' in populate:
                json_row, custom_response = populate_checkins(
                    cursor, item_id, inv_id, owner_id,
                    json_row, custom_response, verbose)

            if 'checkouts' in populate:
                json_row, custom_response = populate_checkouts(
                    cursor, inv_id,
                    json_row,
                    custom_response, verbose)

            if 'cycle_counts' in populate:
                json_row, custom_response = populate_cycle_count(
                    cursor, recent_cycle_count_id,
                    json_row,
                    custom_response, verbose)

            if 'owners' in populate:
                json_row, custom_response = populate_owner(
                    cursor, owner_id,
                    json_row,
                    custom_response, verbose)

            if 'components' in populate and json_row["is_component"]:
                json_row, custom_response = populate_component(
                    cursor, component_id,
                    json_row,
                    custom_response, verbose)

            if 'products' in populate and json_row["is_product"]:
                json_row, custom_response = populate_product(
                    cursor, product_id,
                    json_row,
                    custom_response, verbose)

            inventory[inv_id] = json_row


        # Insert the processed inventory into the response
        custom_response.insert_data(inventory)

        return jsonify(custom_response.to_json()), 200

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()

def populate_checkins(
                    cursor, item_id, inv_id, owner_id,
                    json_row, custom_response, verbose):
    '''
    Populate checkins resources for Inventory Items

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        item_id (int): item ID
        inv_id (int): inventory ID
        owner_id (int): owner ID
        json_row (dict): Row Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        json_row (dict): Row Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'check_in_id', a.`check_in_id`,
                'inv_id', a.`inv_id`,
                'owner_id', a.`owner_id`,
                'item_id', a.`item_id`,
                'courier_id', a.`courier_id`,
                'facility_id', a.`facility_id`,
                'is_product', a.`is_product`,
                'is_component', a.`is_component`,
                'supplier_item_number', a.`supplier_item_number`,
                'lot_number', a.`lot_number`,
                'batch_number', a.`batch_number`,
                'current_status_qty', a.`current_status_qty`,
                'user_id', a.`user_id`,
                'date_entered', a.`date_entered`,
                'date_modified', a.`date_modified`,
                'po_detail_id', a.`po_detail_id`,
                'current_status', a.`current_status`
            )
        AS check_in_objects
        FROM `Inventory`.`Check-in_Log` a
        WHERE 
            a.`item_id` = ? AND
            a.`inv_id` = ? AND
            a.`owner_id` = ?
        '''

        # Execute Query
        cursor.execute(query, (item_id, inv_id, owner_id))
        result = cursor.fetchall()

        # Create Checkins Dictionary
        checkins = {}
        for row in result:
            checkin_json_row = json.loads(row[0])
            check_in_id = checkin_json_row['check_in_id']
            checkins[check_in_id] = checkin_json_row

        json_row['checkins'] = checkins

        # If checkins resource is empty
        if not checkins and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No checkins found for inventory item {json_row["item_name"]} (inventory ID: {inv_id} item ID: {item_id})',
                    message_type=MessageType.WARNING)
            )

        return json_row, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return json_row, custom_response

def populate_checkouts(
        cursor, inv_id,
        json_row, custom_response, verbose):
    '''
    Populate checkins resources for Inventory Items

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        item_id (int): item ID
        inv_id (int): inventory ID
        owner_id (int): owner ID
        json_row (dict): Row Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        json_row (dict): Row Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'check_out_id', a.`check_out_id`,
                'prefix', a.`prefix`,
                'year', a.`year`,
                'month', a.`month`,
                'sec_number', a.`sec_number`,
                'suffix', a.`suffix`,
                'inv_id', a.`inv_id`,
                'lot_number', a.`lot_number`,
                'amount', a.`amount`,
                'user_id', a.`user_id`,
                'date_entered', a.`date_entered`,
                'date_modified', a.`date_modified`,
                'so_detail_id', a.`so_detail_id`,
                'notes', a.`notes`
            )
        AS check_in_objects
        FROM `Inventory`.`Check-out_Log` a
        WHERE 
            a.`inv_id` = ?
        '''

        # Execute Query
        cursor.execute(query, (inv_id,))
        result = cursor.fetchall()

        # Create Checkouts Dictionary
        checkouts = {}
        for row in result:
            checkout_json_row = json.loads(row[0])
            check_out_id = json_row['check_out_id']
            checkouts[check_out_id] = checkout_json_row

        json_row['checkouts'] = checkouts

        # If checkouts resource is empty
        if not checkouts and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No checkouts found for inventory item {json_row["item_name"]} (inventory ID: {inv_id})',
                    message_type=MessageType.WARNING)
            )

        return json_row, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return json_row, custom_response

def populate_cycle_count(cursor, recent_cycle_count_id,
                         json_row,
                         custom_response, verbose):
    '''
    Populate Owner Resource for Inventory Items

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        recent_cycle_count_id (int): recent_cycle_count_id
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        if not recent_cycle_count_id:
            if verbose:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message=f'This item has not been cycle counted',
                        message_type=MessageType.INFO)
                )
            return json_row, custom_response

        query = '''
        SELECT 
            JSON_OBJECT(
                'actual_inventory_precheck', a.`actual_inventory_precheck`,
                'cycle_count_date', a.`cycle_count_date`,
                'amount_counted', a.`amount_counted`,
                'cycle_count_grade', a.`cycle_count_grade`,
                'cycle_counter_user_id', a.`user_id`,
                'fixed_actual_inventory', a.`fixed_actual_inventory`,
                'cycle_count_notes', a.`notes`,
                'cycle_counter_username', b.`username`,
                'cycle_counter_person_id', c.`person_id`,
                'cycle_counter_first_name', c.`first_name`,
                'cycle_counter_last_name', c.`last_name`
            )
        AS cycle_count_object
        FROM `Inventory`.`Cycle_Counts_Log` a
        LEFT JOIN `Organizations`.`Users` b ON
            a.`user_id` = b.`user_id`
        LEFT JOIN `Organizations`.`People` c ON
            b.`person_id` = c.`person_id`
        WHERE 
            a.`cycle_count_id` = ?
        LIMIT 1
        '''

        # Execute Query
        cursor.execute(query, (recent_cycle_count_id,))
        result = cursor.fetchone()

        # If owner resource is empty
        if not result and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'Most cycle count record not found (ID: {json_row["recent_cycle_count_id"]})',
                    message_type=MessageType.WARNING)
            )
        else:
            # Unpack both dicts (** Operator) and merge them together
            json_row = {**json_row, **json.loads(result[0])}

        return json_row, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return json_row, custom_response

def populate_owner(cursor, owner_id, json_row,
                   custom_response, verbose):
    '''
    Populate Owner Resource for Inventory Items

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        owner_id (int): Component ID
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'organization_id', a.`organization_id`, 
                'date_entered', a.`date_entered`,
                'website_url', a.`website_url`,
                'vetted', a.`vetted`,
                'date_vetted', a.`date_vetted`,
                'risk_level', a.`risk_level`,
                'supplier', a.`supplier`,
                'client', a.`client`,
                'lab', a.`lab`,
                'courier', a.`courier`,
                'other', a.`other`,
                'notes', a.`notes`,
                'organization_name', b.`organization_name`,
                'organization_initial', b.`organization_initial`
            )
        AS organizaiton_object
        FROM `Organizations`.`Organizations` a
        LEFT JOIN `Organizations`.`Organization_Names` b ON
            a.`organization_id` = b.`organization_id`
        WHERE 
            a.`organization_id` = ?
        LIMIT 1
        '''

        # Execute Query
        cursor.execute(query, (owner_id,))
        result = cursor.fetchone()

        # If owner resource is empty
        if not result and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'Owner not found (ID: {json_row["owner_id"]})',
                    message_type=MessageType.WARNING)
            )
        else:
            # Unpack both dicts (** Operator) and merge them together
            json_row = {**json_row, **json.loads(result[0])}

        return json_row, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return json_row, custom_response

def populate_component(cursor, component_id, json_row,
                        custom_response, verbose):
    '''
    Populate Components Resource for Inventory Items

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        component_id (int): Component ID
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'brand_id', a.`brand_id`,
                'component_type', a.`component_type`,
                'units', a.`units`,
                'date_entered', a.`date_entered`,
                'certified_usda_organic', a.`certified_usda_organic`,
                'certified_halal', a.`certified_halal`,
                'certified_kosher', a.`certified_kosher`,
                'certified_gluten_free', a.`certified_gluten_free`,
                'certified_national_sanitation_foundation', a.`certified_national_sanitation_foundation`,
                'certified_us_pharmacopeia', a.`certified_us_pharmacopeia`,
                'certified_non_gmo', a.`certified_non_gmo`,
                'certified_vegan', a.`certified_vegan`,
                'brand_name', c.`organization_name`,
                'brand_initial', c.`organization_initial`,
                'brand_website', b.`website_url`
            )
        AS component_object
        FROM `Inventory`.`Components` a
        LEFT JOIN `Organizations`.`Organizations` b ON
            a.`brand_id` = b.`organization_id`
        LEFT JOIN `Organizations`.`Organization_Names` c ON
            a.`brand_id` = c.`organization_id`
        WHERE 
            a.`component_id` = ?
        LIMIT 1
        '''

        # Execute Query
        cursor.execute(query, (component_id,))
        result = cursor.fetchone()

        # If components resource is empty
        if not result and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'Component not found (ID: {json_row["component_id"]})',
                    message_type=MessageType.WARNING)
            )
        else:
            # Unpack both dicts (** Operator) and merge them together
            json_row = {**json_row, **json.loads(result[0])}

        return json_row, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return json_row, custom_response

def populate_product(cursor, product_id, json_row,
                        custom_response, verbose):
    '''
    Populate Components Resource for Inventory Items

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        product_id (int): Product ID
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        json_row (dict): Item Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query='''
        SELECT
            JSON_OBJECT(
                'product_type', a.`type`,
                'current_product', a.`current_product`,
                'date_entered', a.`date_entered`,
                'spec_issue_date', a.`spec_issue_date`,
                'spec_revise_date', a.`spec_revise_date`,
                'exp_time_frame', a.`exp_time_frame`,
                'exp_unit', a.`exp_unit`,
                'exp_type', a.`exp_type`,
                'exp_use_oldest_ingredient', a.`exp_use_oldest_ingredient`,
                'default_formula_id', a.`default_formula_id`,
                'certified_usda_organic', a.`certified_usda_organic`,
                'certified_halal', a.`certified_halal`,
                'certified_kosher', a.`certified_kosher`,
                'certified_gluten_free', a.`certified_gluten_free`,
                'certified_national_sanitation_foundation', a.`certified_national_sanitation_foundation`,
                'certified_us_pharmacopeia', a.`certified_us_pharmacopeia`,
                'certified_non_gmo', a.`certified_non_gmo`,
                'certified_vegan', a.`certified_vegan`
            )
        AS product_object
        FROM `Products`.`Product_Master` a
        LEFT JOIN `Organizations`.`Organizations` b ON
            a.`organization_id` = b.`organization_id`
        LEFT JOIN `Organizations`.`Organization_Names` c ON
            a.`organization_id` = c.`organization_id`
        WHERE
            a.`product_id` = ?
        LIMIT 1
        '''

        # Execute Query
        cursor.execute(query, (product_id,))
        result=cursor.fetchone()[0]

        # If components resource is empty
        if not result and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'Product not found (ID: {json_row["product_id"]})',
                    message_type=MessageType.WARNING)
            )
        else:
            # Unpack both dicts (** Operator) and merge them together
            json_row = {**json_row, **json.loads(result[0])}

        return json_row, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return json_row, custom_response

@bp.route('/checkin', methods=['POST', 'PUT'])
@check_authenticated(authentication_required=True)
def checkin():
    """
    Handle Checkin

    The request body must contain the following
    fields in the form-data.

    form-data:
        (One or the other, not both)
        component_id: (int)
        product_id: (int)

        courier_id: (int) This key field is required, but can be set to 0
        facility_id: (int) This key field is required, but can be set to 0,
                    facility_id must be > 0 if courier_id is > 0
        owner_id: (int)
        supplier_item_number: (str) (optional)
        lot_number: (str) (optional)
        batch_number: (str) (optional)
        current_status_qty: (int or float)
        po_detail_id: (int) (optional)
        current_status: (str)
           ENUM: (
               'Ordered',  (POST ONLY)
               'In Transit',
               'Received',
               'Quarantined',
               'Canceled',
               'Shipment Missing',
               'Revised Order Decreased',
               'Revised Order Increased',
               'Released from Quarantine',
               'Found',  (POST ONLY)
               'Produced'  (POST ONLY)
            )
        status_notes: (str) (optional)
        doc: (list of document detail objects)
             (required if files are uploaded)
            document detail object template: {
                "id": "file_#",
                "filename": "test_doc.pdf",
                "name": "test_doc",
                "extention": ".pdf",
                "description": "This is a test document",
                "document_type": "testing"
            }
        file_#: (file)
                (required if files are uploaded)
    """

    try:
        custom_response = CustomResponse()  # create a custom response object

        ### Validate Form Data ###
        form_data = dict(request.form)
        valid, custom_response = validate_checkin_form(request, custom_response)
        if not valid:
            return jsonify(custom_response.to_json()), 400

        ### Connect to MariaDB ###
        try:
            # Test DB Connection
            mariadb_connection = mariadb.connect(
                host=app.config['DB_HOSTNAME'],
                port=int(app.config['DB_PORT']),
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD']
            )

        except mariadb.Error as mariadb_error:
            print(f"Error connecting to the database: {mariadb_error}")
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Failed to connect to MariaDB",
                    message_type=MessageType.DANGER
                )
            )
            return jsonify(custom_response.to_json()), 500

        mariadb_connection.autocommit = False  # Begin Transaction

        ### Get inv_id, Create inv_id if None exists ###
        inv_id, custom_response = get_inventory_id(
            mariadb_connection, request, custom_response)
        if not inv_id:
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500

        ### Update `Inventory`.`Check-in_Log` Table ###
        cursor = mariadb_connection.cursor()

        # Get check_in_id, Create check_in_id if None exists
        inserted_check_in_id = None
        updated_check_in_id = None
        if request.method == 'POST':
            # Create Checkin id
            base_query_1a = '''
                SELECT `check_in_id`
                FROM `Inventory`.`Check-in_Log`
                ORDER BY
                    `check_in_id` DESC
                LIMIT 1
            '''
            cursor.execute(base_query_1a)
            result = cursor.fetchone()
            if not result:
                result = [0]
            check_in_id = result[0] + 1

            # This function creates directories and saves files
            # if the request contains file objects.  It will delete
            # the entire directory if the transaction fails.
            inserted_check_in_id, custom_response = insert_check_in_log(
                mariadb_connection, check_in_id,
                inv_id, request, custom_response)

        else:
            # Validate check_in_id
            base_query_1b = '''
                SELECT `check_in_id`
                FROM `Inventory`.`Check-in_Log`
                WHERE `check_in_id` = ?
                LIMIT 1
            '''
            cursor.execute(base_query_1b, (form_data["check_in_id"],))
            result = cursor.fetchone()

            if not result:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="Invalid check_in_id",
                        message_type=MessageType.DANGER
                    )
                )
                return jsonify(custom_response.to_json()), 400

            # The PUT method must have a check_in_id field
            check_in_id = form_data["check_in_id"]

            # This function creates directories and saves files
            # if the request contains file objects.  It will delete
            # the entire directory if the transaction fails.
            updated_check_in_id, custom_response = update_check_in_log(
                mariadb_connection, check_in_id,
                inv_id, request, custom_response)

            if not updated_check_in_id:
                return jsonify(custom_response.to_json()), 400

        if not (inserted_check_in_id or updated_check_in_id):
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500
        mariadb_connection.commit()
        return jsonify(custom_response.to_json()), 200

    except Exception:
        if 'mariadb_connection' in locals():
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
    Handle Checkout

    The request body must contain the following
    fields in the form-data.

    form-data:
        (One or the other, not both)
        component_id: (int)
        product_id: (int)

        courier_id: (int) This key field is required, but can be set to 0
        facility_id: (int) This key field is required, but can be set to 0,
                    facility_id must be > 0 if courier_id is > 0
        owner_id: (int)
        supplier_item_number: (str) (optional)
        lot_number: (str) (optional)
        batch_number: (str) (optional)
        current_status_qty: (int or float)
        po_detail_id: (int) (optional)
        current_status: (str)
           ENUM: (
               'Ordered',  (POST ONLY)
               'In Transit',
               'Received',
               'Quarantined',
               'Canceled',
               'Shipment Missing',
               'Revised Order Decreased',
               'Revised Order Increased',
               'Released from Quarantine',
               'Found',  (POST ONLY)
               'Produced'  (POST ONLY)
            )
        status_notes: (str) (optional)
        doc: (list of document detail objects)
             (required if files are uploaded)
            document detail object template: {
                "id": "file_#",
                "filename": "test_doc.pdf",
                "name": "test_doc",
                "extention": ".pdf",
                "description": "This is a test document",
                "document_type": "testing"
            }
        file_#: (file)
                (required if files are uploaded)
    """

    try:
        custom_response = CustomResponse()  # create a custom response object

        ### Validate Form Data ###
        form_data = dict(request.form)
        valid, custom_response = validate_checkin_form(
            request, custom_response)
        if not valid:
            return jsonify(custom_response.to_json()), 400

        ### Connect to MariaDB ###
        try:
            # Test DB Connection
            mariadb_connection = mariadb.connect(
                host=app.config['DB_HOSTNAME'],
                port=int(app.config['DB_PORT']),
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD']
            )

        except mariadb.Error as mariadb_error:
            print(f"Error connecting to the database: {mariadb_error}")
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Failed to connect to MariaDB",
                    message_type=MessageType.DANGER
                )
            )
            return jsonify(custom_response.to_json()), 500

        mariadb_connection.autocommit = False  # Begin Transaction

        ### Get inv_id, Create inv_id if None exists ###
        inv_id, custom_response = get_inventory_id(
            mariadb_connection, request, custom_response)
        if not inv_id:
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500

        ### Update `Inventory`.`Check-in_Log` Table ###
        cursor = mariadb_connection.cursor()

        # Get check_in_id, Create check_in_id if None exists
        inserted_check_in_id = None
        updated_check_in_id = None
        if request.method == 'POST':
            # Create Checkin id
            base_query_1a = '''
                SELECT `check_in_id`
                FROM `Inventory`.`Check-in_Log`
                ORDER BY
                    `check_in_id` DESC
                LIMIT 1
            '''
            cursor.execute(base_query_1a)
            result = cursor.fetchone()
            if not result:
                result = [0]
            check_in_id = result[0] + 1

            # This function creates directories and saves files
            # if the request contains file objects.  It will delete
            # the entire directory if the transaction fails.
            inserted_check_in_id, custom_response = insert_check_in_log(
                mariadb_connection, check_in_id,
                inv_id, request, custom_response)

        else:
            # Validate check_in_id
            base_query_1b = '''
                SELECT `check_in_id`
                FROM `Inventory`.`Check-in_Log`
                WHERE `check_in_id` = ?
                LIMIT 1
            '''
            cursor.execute(base_query_1b, (form_data["check_in_id"],))
            result = cursor.fetchone()

            if not result:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="Invalid check_in_id",
                        message_type=MessageType.DANGER
                    )
                )
                return jsonify(custom_response.to_json()), 400

            # The PUT method must have a check_in_id field
            check_in_id = form_data["check_in_id"]

            # This function creates directories and saves files
            # if the request contains file objects.  It will delete
            # the entire directory if the transaction fails.
            updated_check_in_id, custom_response = update_check_in_log(
                mariadb_connection, check_in_id,
                inv_id, request, custom_response)

            if not updated_check_in_id:
                return jsonify(custom_response.to_json()), 400

        if not (inserted_check_in_id or updated_check_in_id):
            mariadb_connection.rollback()
            return jsonify(custom_response.to_json()), 500
        mariadb_connection.commit()
        return jsonify(custom_response.to_json()), 200

    except Exception:
        if 'mariadb_connection' in locals():
            mariadb_connection.rollback()
        error = error_message()
        custom_response.insert_flash_message(error)
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()

def validate_checkin_form(request, custom_response):
    """
    Does a basic validation check on the request form data
    from the checkin form.

    Parameters:
        request: (flask.request)
        custom_response: (CustomResponse)

    Returns:
        valid: (bool)
        custom_response: (CustomResponse)

    Upon Failure:
        Returns False, custom_response
        updating the custom_response object with all the
        error messages
    """

    form_data = dict(request.form)

    # Validate current_status_qty
    valid = True
    if not validate_float_in_dict(form_data, 'current_status_qty'):
        custom_response.insert_form_message(
            form_id=0,
            message=Message(
                message="Invalid current_status_qty",
                message_type=MessageType.DANGER
            )
        )
        valid = False

    # Validate item_id
    if not (validate_int_in_dict(form_data, 'component_id') or \
    validate_int_in_dict(form_data, 'product_id')):
        custom_response.insert_form_message(
            form_id=1,
            message=Message(
                message="Invalid item_id",
                message_detail="Item_id must be an int with the key of product_id or component_id",
                message_type=MessageType.DANGER
            )
        )
        valid = False

    # validate owner_id
    if not validate_int_in_dict(form_data, 'owner_id'):
        custom_response.insert_form_message(
            form_id=2,
            message=Message(
                message="Invalid owner_id",
                message_type=MessageType.DANGER
            )
        )
        valid = False

    # validate courier_id
    if not validate_int_in_dict(form_data, 'courier_id'):
        custom_response.insert_form_message(
            form_id=2,
            message=Message(
                message="Invalid courier_id",
                message_type=MessageType.DANGER
            )
        )
        valid = False
    else:
        if int(form_data["courier_id"]) > 0:
            # validate facility_id
            if not validate_int_in_dict(form_data, 'facility_id'):
                custom_response.insert_form_message(
                    form_id=2,
                    message=Message(
                        message="Invalid facility_id",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False

            if not (int(form_data["courier_id"]) > 0 and \
                int(form_data["facility_id"]) > 0):
                custom_response.insert_form_message(
                    form_id=3,
                    message=Message(
                        message="Invalid facility_id",
                        message_detail="facility_id must be provided with courier_id",
                        message_type=MessageType.DANGER
                    )
                )
                valid = False
            else:
                valid, custom_response = check_facility_id_related_org_id(form_data["courier_id"], form_data["facility_id"], custom_response)

    # Validate current_status
    if request.method == 'POST':
        if "current_status" not in form_data.keys() or \
            form_data["current_status"] not in [
            'Ordered',
            'In Transit',
            'Received',
            'Found',
            'Produced'
        ]:
            custom_response.insert_form_message(
                form_id=5,
                message=Message(
                    message="Invalid checkin status",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

    if request.method == 'PUT':

        if not validate_int_in_dict(form_data, 'check_in_id', equal_to=False):
            custom_response.insert_form_message(
                form_id=6,
                message=Message(
                    message="Invalid check_in_id",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

        if "current_status" not in form_data.keys() or \
            form_data["current_status"] not in [
            'Revised Order Increased',
            'Revised Order Decreased',
            'In Transit',
            'Received',
            'Found',
            'Produced',
            'Missing Shipment',
            'Canceled',
            'Quarantined',
            'Released from Quarantine'
        ]:
            custom_response.insert_form_message(
                form_id=7,
                message=Message(
                    message="Invalid checkin status",
                    message_type=MessageType.DANGER
                )
            )
            valid = False

    return valid, custom_response

def validate_checkout_form(request, custom_response):
    form_data = dict(request.form)
    # Validate form data
    valid = True
    if not validate_float_in_dict(form_data, 'current_status_qty'):
        custom_response.insert_flash_message(
            FlashMessage(
                message="Invalid current_status_qty",
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
        return None, custom_response
    else:
        return True, custom_response

def get_inventory_id(mariadb_connection, request, custom_response):
    """
    Returns the inventory id for the item if found,
    otherwise creates a new one.

    Parameters:
        mariadb_connection (object): MariaDB connection object
        request (object): Flask request object
        custom_response (object): Flask response object

    Returns:
        inv_id (int): Inventory Id
        custom_response (object): Flask response object

    Upon Failure:
        Returns None, custom_response
        updating the custom_response object with error message
    """

    try:
        form_data = dict(request.form)

        # Locate the component in the `Inventory`.`Inventory` table
        base_query_1 = """
            SELECT 
                `inv_id`,
                `item_id`,
                `owner_id`
            FROM `Inventory`.`Inventory`
            WHERE `item_id` = ? AND `owner_id` = ?
        """

        # Execute Query
        cursor = mariadb_connection.cursor()
        inputs = []

        # item_id
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        inputs.append(item_id)

        # owner_id
        inputs.append(form_data["owner_id"])
        cursor.execute(base_query_1, tuple(inputs))
        result = cursor.fetchone()

        if result:
            inv_id = result[0]

        else:
            # If component not found in `Inventory`.`Inventory`
            # table, create a new record
            inv_id, custom_response = post_item_to_inventory(
                mariadb_connection,
                request, custom_response
            )
            if inv_id:
                return inv_id, custom_response
            else:
                None, custom_response

        return inv_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def post_item_to_inventory(mariadb_connection, request, custom_response):
    """
    Posts a new item to the `Inventory`.`Inventory` table.

    Parameters:
        mariadb_connection (object): MariaDB connection object
        request (object): Flask request object
        custom_response (object): Flask response object

    Returns:
        inv_id (int): Inventory Id
        custom_response (object): Flask response object

    Upon Failure:
        Returns None, custom_response
        updating the custom_response object with error message
    """

    try:
        form_data = dict(request.form)

        # Build Insert Statement
        base_query = """
        INSERT INTO `Inventory`.`Inventory` (
            `item_id`,
            `owner_id`,
            `is_component`,
            `is_product`,
            `actual_inventory`,
            `theoretical_inventory`,
            `recent_cycle_count_id`
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?
        )
        """

        inputs = []

        # item_id
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        inputs.append(item_id)

        # owner_id
        inputs.append(form_data["owner_id"])

        # is_component & is_product
        if "component_id" in form_data.keys():
            inputs.append(True)
            inputs.append(False)
        elif "product_id" in form_data.keys():
            inputs.append(False)
            inputs.append(True)
        else:
            inputs.append(False)
            inputs.append(False)

        # actual_inventory & theoretical_inventory
        inputs.append(0)
        inputs.append(0)

        # recent_cycle_count_id
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

def get_item_type(mariadb_connection, request, custom_response):
    """
    Get the item type based on the request component_id or product_id.

    Parameters:
        mariadb_connection (obj): MariaDB Connection Object
        request (obj): Flask Request Object
        custom_response (obj): Flask Response Object

    Returns:
        item_type (str): Item Type
        custom_response (obj): Flask Response Object

    Upon Failure:
        Returns: None, custom_response
        updating the custom_response object with error message
    """

    try:
        form_data = dict(request.form)

        if 'component_id' in form_data.keys():

            # Build Query Statement
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
            item_type = cursor.fetchone()[0]

            return item_type, custom_response

        elif 'product_id' in form_data.keys():

            # Build Query Statement
            base_query = """
            SELECT
                `product_id`
            FROM 
                `Products`.`Product_Master`
            WHERE
                `product_id` = ?
            LIMIT 1
            """

            inputs = []
            inputs.append(form_data["product_id"])

            # Execute Statement
            cursor = mariadb_connection.cursor()
            cursor.execute(base_query, tuple(inputs))
            product_id = cursor.fetchone()[0]
            if product_id:
                return "product", custom_response
            else:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="Invalid product_id.",
                        message_type=MessageType.DANGER
                    )
                )
                return None, custom_response

        else:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid item_id Key",
                    message_detail="Could not find item_type",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def insert_check_in_log(mariadb_connection, check_in_id, inv_id, request, custom_response):
    """
    Inserts a new checkin log to the `Inventory`.`Check_In_Log` table.

    Parameters:
        mariadb_connection (object): MariaDB connection object
        check_in_id (int): Check In Id
        inv_id (int): Inventory Id
        request (object): Flask request object
        custom_response (object): Flask response object

    Returns:
        check_in_id (int): New Check In Id
        custom_response (object): Flask response object

    Upon Failure:
        Returns None, custom_response
        Updating the custom_response object with error message
    """

    try:
        cursor = mariadb_connection.cursor()
        form_data = dict(request.form)

        ### Prepare Save Files ###

        # Check `Inventory`.`Components` or
        # `Products`.`Product_Master` tables
        # and get the item_type
        item_type, custom_response = get_item_type(
            mariadb_connection,
            request,
            custom_response
        )

        # If the Item does not exist in the `Inventory`.`Components`
        # or `Products`.`Product_Master` tables,
        # fail the checkin and report to the user.
        if not item_type:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid component.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response


        file_objects = dict(request.files)

        if "doc" in form_data:
            doc = json.loads(form_data["doc"])
        else:
            doc = []

        # Create a location link for files related to this checkin
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        location = \
            item_type + "/" + \
            str(item_id_dir) + "/" \
            "inv_id-" + str(inv_id) + "/" \
            "check_in_id-" + str(check_in_id) + "/" + \
            "status-" + str(form_data["current_status"]) + \
            "  date-" + \
            str(datetime.utcnow().strftime("Y%Y-M%m-D%d H%H-M%M-S%S"))
        rollback_location = \
            item_type + "/" + str(item_id_dir) + "/"

        # Save Files
        doc, custom_response = save_files(
            doc, file_objects, custom_response, location)

        ### Create New Checkin Log ###

        # Build Insert Statement
        base_query_3 = '''
            INSERT INTO `Inventory`.`Check-in_Log` (
                `check_in_id`,
                `inv_id`,
                `owner_id`,
                `item_id`,
                `courier_id`,
                `facility_id`,
                `is_product`,
                `is_component`,
                `supplier_item_number`,
                `lot_number`,
                `batch_number`,
                `current_status_qty`,
                `user_id`,
                `po_detail_id`,
                `current_status`,
                `current_status_notes`,
                `doc`
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
            )
        '''

        # Gather Inputs
        inputs = []
        inputs.append(check_in_id)
        inputs.append(inv_id)

        # owner_id
        inputs.append(form_data['owner_id'])

        # item_id
        inputs.append(item_id)

        # courier_id
        if "courier_id" in form_data.keys() and \
                int(form_data["courier_id"]) > 0:
            inputs.append(form_data["courier_id"])

            # facility_id
            if "facility_id" in form_data.keys() and \
                    int(form_data["facility_id"]) > 0:
                inputs.append(form_data["facility_id"])
            else:
                raise ValueError
        else:
            inputs.append(None)
            inputs.append(None)

        # is_product & is_component
        if "product_id" in form_data.keys():
            inputs.append(True)
            inputs.append(False)
        elif "component_id" in form_data.keys():
            inputs.append(False)
            inputs.append(True)
        else:
            inputs.append(False)
            inputs.append(False)

        # supplier_item_number
        if 'supplier_item_number' in form_data.keys():
            inputs.append(form_data["supplier_item_number"])
        else:
            inputs.append(None)

        # lot_number
        if 'lot_number' in form_data.keys():
            inputs.append(form_data["lot_number"])
        else:
            inputs.append(None)

        # batch_number
        if 'batch_number' in form_data.keys():
            inputs.append(form_data["batch_number"])
        else:
            inputs.append(None)

        # current_status_qty
        inputs.append(form_data["current_status_qty"])

        # user_id
        session_token = request.cookies.get('session')
        redis_connection = Redis(
            host=app.config['REDIS_HOST'],
            port=app.config['REDIS_PORT'],
            password=app.config['REDIS_PASSWORD'])
        session_data = json.loads(redis_connection.get(session_token))
        inputs.append(session_data["user_id"])
        # Note: redis_connection automatically closes the connection

        # po_detail_id
        if 'po_detail_id' in form_data.keys():
            inputs.append(form_data["po_detail_id"])
        else:
            inputs.append(None)

        # current status
        inputs.append(form_data["current_status"])

        # curent_status_notes
        if "current_status_notes" in form_data.keys():
            current_status_notes = form_data["current_status_notes"]
        else:
            current_status_notes = ""
        inputs.append(current_status_notes)

        # doc
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
                    "actual_before_change": 0,
                    "theoretic_before_change": 0,
                    "qty_changing": form_data["current_status_qty"],
                    "previous_status": "NULL"
                }
            ]
        }))

        cursor.execute(base_query_3, tuple(inputs))

        # Confirm that checkin record was successfully saved in
        # the `Inventory`.`Check-in_Log` table
        check_query = """
            SELECT 
                `inv_id`, 
                `item_id`,
                `owner_id`,
                `doc`
            FROM
                `Inventory`.`Check-in_Log`
            WHERE 
                `inv_id` = ? AND
                `item_id` = ? AND
                `owner_id` = ?
        """
        inputs_c = []

        # inv_id  (Where Clause)
        inputs_c.append(inv_id)

        # item_id  (Where Clause)
        inputs_c.append(item_id)

        # owner_id  (Where Clause)
        inputs_c.append(form_data["owner_id"])

        cursor.execute(check_query, tuple(inputs_c))
        result = cursor.fetchone()

        if not result:
            # If insert statement fails, rolback and return error
            flash_message = FlashMessage(
                    message="Failed to create new checkin log",
                    message_type=MessageType.DANGER
                )

            # Rollback/Delete Saved Directory with Files
            deleted, custom_response = delete_directory(
                rollback_location, custom_response, flash_message)
            mariadb_connection.rollback()
            return None, custom_response

        ### Update `Inventory`.`Inventory` Table ###

        inv_changed = False
        if form_data["current_status"] in [
                "Ordered",
                "In Transit"
            ]:
            inv_changed, custom_response = add_theoretic_inventory(
                mariadb_connection, inv_id, request, custom_response)

        if form_data["current_status"] in [
                "Received",
                "Found"
            ]:
            inv_changed, custom_response = add_actual_inventory(
                mariadb_connection, inv_id, request, custom_response)

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
            # Rollback/Delete Saved Directory with Files
            deleted, custom_response = delete_directory(
                rollback_location, custom_response)
            mariadb_connection.rollback()
            return None, custom_response

        return check_in_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        # Rollback/Delete Saved Directory with Files
        deleted, custom_response = delete_directory(
            rollback_location, custom_response)
        mariadb_connection.rollback()
        return None, custom_response

def update_check_in_log(mariadb_connection, check_in_id, inv_id, request, custom_response):
    """
    Updates checkin log in the `Inventory`.`Check_In_Log` table.

    Parameters:
        mariadb_connection (obj): MariaDB connection object.
        check_in_id (int): Checkin ID.
        inv_id (int): Inventory ID.
        request (obj): Flask request object.
        custom_response (obj): CustomResponse object.

    Returns:
        check_in_id (int): Checkin ID.
        custom_response (obj): CustomResponse object.

    Upon Failure:
        Returns None, custom_response.
        updating custom_response with error message.
    """

    try:

        cursor = mariadb_connection.cursor()
        form_data = dict(request.form)

        # Check `Inventory`.`Components` or
        # `Products`.`Product_Master` tables
        # and get the item_type
        item_type, custom_response = get_item_type(
            mariadb_connection,
            request,
            custom_response
        )

        # If the Item does not exist in the `Inventory`.`Components`
        # or `Products`.`Product_Master` tables,
        # fail the checkin and report to the user.
        if not item_type:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Invalid component.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response

        # Find most recent/previous checkin status
        base_query = '''
            SELECT
                `check_in_id`,
                `inv_id`,
                `owner_id`,
                `item_id`,
                `current_status`
            FROM
                `Inventory`.`Check-in_Log`
            WHERE
                `check_in_id` = ? AND 
                `inv_id` = ? AND 
                `owner_id` = ? AND 
                `item_id` = ?
            LIMIT 1
        '''

        inputs = []
        inputs.append(check_in_id)
        inputs.append(inv_id)

        # owner_id
        inputs.append(form_data['owner_id'])

        # item_id
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        inputs.append(item_id)

        cursor.execute(base_query, tuple(inputs))
        result = cursor.fetchone()
        if result:
            previous_status = result[4]
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

        # Get current inventory before changes are made while
        # checking that inventory record exists.
        inventory_row, custom_response = get_inventory_for_single_record(
            mariadb_connection, inv_id, custom_response
        )
        if not inventory_row:
            custom_response.insert_flash_message(
                FlashMessage(
                    message="Failed to find inventory record.",
                    message_detail="Inventory record not found. Talk to IT Support.",
                    message_type=MessageType.DANGER
                )
            )
            return None, custom_response

        ### Compare Previous and Current Status ###
        invalid_status_update_message = FlashMessage(
            message="Checkin status did not change.",
            message_detail="Previous status: '" + previous_status +
            "', Current status: '" + current_status + "' is an invalid status update.",
            message_type=MessageType.DANGER
        )

        inv_changed = False
        required_inv_change = False

        if previous_status == "Ordered":
            if current_status not in [
                "Received",
                "Missing Shipment",
                "Canceled",
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
                "Revised Order Decreased"
            ]:
                inv_changed, custom_response = remove_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
                required_inv_change = True
            if current_status == "Revised Order Increased":
                inv_changed, custom_response = add_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
                required_inv_change = True
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
                required_inv_change = True

        elif previous_status == "Revised Order Increased" or \
        previous_status == "Revised Order Decreased":
            if current_status not in [
                "Received",
                "Missing Shipment",
                "Canceled",
                "In Transit"
            ]:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response
            if current_status in [
                "Received",
                "Missing Shipment",
                "Canceled"
            ]:
                inv_changed, custom_response = remove_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
                required_inv_change = True
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
                required_inv_change = True

        elif previous_status == "In Transit":
            if current_status not in [
                "Received",
                "Missing Shipment",
                "Canceled"
            ]:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response
            if current_status in [
                "Received",
                "Missing Shipment",
                "Canceled"
            ]:
                inv_changed, custom_response = remove_theoretic_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            required_inv_change = True

        elif previous_status == "Received":
            required_inv_change = True
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
                "Canceled"
            ]:
                custom_response.insert_flash_message(
                    invalid_status_update_message
                )
                return None, custom_response
            if current_status == "Received":
                inv_changed, custom_response = add_actual_inventory(
                    mariadb_connection, inv_id, request, custom_response)
            required_inv_change = True

        elif previous_status == "Found" or previous_status == "Produced":
            required_inv_change = True
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
            required_inv_change = True
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
            required_inv_change = True
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
            if required_inv_change:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="No inventory changes were made.",
                        message_detail="Failed to make required inventory changes.",
                        message_type=MessageType.DANGER
                    )
                )
                return None, custom_response

            else:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message="No inventory changes were made.",
                        message_type=MessageType.INFO
                    )
                )

        # Get current doc from checkin log
        base_query_2 = '''
            SELECT
                `doc`
            FROM 
                `Inventory`.`Check-in_Log`
            WHERE
                `check_in_id` = ? AND
                `inv_id` = ? AND
                `owner_id` = ? AND
                `item_id` = ?
            LIMIT 1
        '''

        inputs = []
        inputs.append(check_in_id)
        inputs.append(inv_id)

        # owner_id
        inputs.append(form_data['owner_id'])

        # item_id
        inputs.append(item_id)

        cursor.execute(base_query_2, tuple(inputs))
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
            item_type + "/" + \
            str(item_id_dir) + "/" \
            "inv_id-" + str(inv_id) + "/" \
            "check_in_id-" + str(check_in_id) + "/" + \
            "status-" + str(form_data["current_status"]) + \
            "  date-" + str(datetime.utcnow().strftime("Y%Y-M%m-D%d H%H-M%M-S%S"))
        doc, custom_response = save_files(
            doc, file_objects, custom_response, location)

        # Create new doc data
        new_doc_files = current_doc["files"] + doc
        if "current_status_notes" in form_data.keys():
            current_status_notes = form_data["current_status_notes"]
        else:
            current_status_notes = ""
        current_doc["status_history"].append({
            "current_status": current_status,
            "status_notes": current_status_notes,
            "actual_before_change": float(inventory_row[5]),
            "theoretic_before_change": float(inventory_row[6]),
            "qty_changing": form_data["current_status_qty"],
            "previous_status": previous_status
        })
        new_doc = current_doc.copy()
        new_doc["files"] = new_doc_files

        ### Update Checkin Log ###

        # Build Update Statement
        base_query_3 = '''
            UPDATE `Inventory`.`Check-in_Log`
            SET
                `courier_id` = ?,
                `facility_id` = ?,
                `supplier_item_number` = ?,
                `lot_number` = ?,
                `batch_number` = ?,
                `po_detail_id` = ?,
                `current_status` = ?,
                `current_status_notes` = ?,
                `current_status_qty` = ?,
                `doc` = ?
            WHERE
                `check_in_id` = ? AND
                `inv_id` = ? AND
                `owner_id` = ? AND
                `item_id` = ?
        '''

        # Gather Inputs
        inputs = []

        # courier_id
        if "courier_id" in form_data.keys() and \
                int(form_data["courier_id"]) > 0:
            inputs.append(form_data["courier_id"])

            # facility_id
            if "facility_id" in form_data.keys() and \
                    int(form_data["facility_id"]) > 0:
                inputs.append(form_data["facility_id"])
            else:
                raise ValueError
        else:
            inputs.append(None)
            inputs.append(None)

        # supplier_item_number
        if 'supplier_item_number' in form_data.keys():
            inputs.append(form_data["supplier_item_number"])
        else:
            inputs.append(None)

        # lot_number
        if 'lot_number' in form_data.keys():
            inputs.append(form_data["lot_number"])
        else:
            inputs.append(None)

        # batch_number
        if 'batch_number' in form_data.keys():
            inputs.append(form_data["batch_number"])
        else:
            inputs.append(None)

        # po_detail_id
        if 'po_detail_id' in form_data.keys():
            inputs.append(form_data["po_detail_id"])
        else:
            inputs.append(None)

        # current_status
        inputs.append(current_status)

        # current_status_notes
        if "current_status_notes" in form_data.keys():
            inputs.append(form_data["current_status_notes"])
        else:
            inputs.append("")

        # current_status_qty
        inputs.append(form_data["current_status_qty"])

        # doc
        inputs.append(json.dumps(new_doc))

        # check_in_id
        inputs.append(check_in_id)

        # inv_id
        inputs.append(inv_id)

        # owner_id
        inputs.append(form_data['owner_id'])

        # item_id
        inputs.append(item_id)

        # Execute Statement
        cursor.execute(base_query_3, tuple(inputs))

        if not result:
            # If insert statement fails, rolback and return error
            flash_message = FlashMessage(
                message="Failed to create new checkin log",
                message_type=MessageType.DANGER
            )

            # Rollback/Delete Saved Directory with Files
            deleted, custom_response = delete_directory(
                    location, custom_response, flash_message)
            mariadb_connection.rollback()
            return None, custom_response
        return check_in_id, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        # Rollback/Delete Saved Directory with Files
        deleted, custom_response = delete_directory(
            location, custom_response)
        mariadb_connection.rollback()
        return None, custom_response

def insert_check_out_log(mariadb_connection, check_out_id, request, custom_response):
    raise NotImplementedError

def update_check_out_log(mariadb_connection, check_out_id, request, custom_response):
    raise NotImplementedError

def add_actual_inventory(mariadb_connection, inv_id, request, custom_response):
    """
    Adds to actual inventory.

    Parameters:
        mariadb_connection (object): MariaDB Connection Object
        inv_id (int): Inventory ID
        request (object): Flask Request Object
        custom_response (object): Flask Response Object

    Returns:
        (bool): True if successful, False otherwise
        custom_response (object): Flask Response Object

    Upon Failure:
        Returns: False, custom_response
        updating the custom_response object with error message
    """

    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `actual_inventory` = `actual_inventory` + ?
            WHERE
                `inv_id` = ? AND `item_id` = ? AND `owner_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["current_status_qty"]))
        inputs.append(inv_id)

        form_data = dict(request.form)

        # item_id
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        inputs.append(item_id)

        # owner_id
        inputs.append(form_data["owner_id"])

        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def remove_actual_inventory(mariadb_connection, inv_id, request, custom_response):
    """
    Removes from actual inventory.

    Parameters:
        mariadb_connection (object): MariaDB Connection Object
        inv_id (int): Inventory ID
        request (object): Flask Request Object
        custom_response (object): Flask Response Object

    Returns:
        (bool): True if successful, False otherwise
        custom_response (object): Flask Response Object

    Upon Failure:
        Returns: False, custom_response
        updating the custom_response object with error message
    """

    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `actual_inventory` = `actual_inventory` - ?
            WHERE
                `inv_id` = ? AND `item_id` = ? AND `owner_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["current_status_qty"]))
        inputs.append(inv_id)

        form_data = dict(request.form)

        # item_id
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        inputs.append(item_id)

        # owner_id
        inputs.append(form_data["owner_id"])

        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def add_theoretic_inventory(mariadb_connection, inv_id, request, custom_response):
    """
    Adds to theoretic inventory.

    Parameters:
        mariadb_connection (object): MariaDB Connection Object
        inv_id (int): Inventory ID
        request (object): Flask Request Object
        custom_response (object): Flask Response Object

    Returns:
        (bool): True if successful, False otherwise
        custom_response (object): Flask Response Object

    Upon Failure:
        Returns: False, custom_response
        updating the custom_response object with error message
    """

    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `theoretical_inventory` = `theoretical_inventory` + ?
            WHERE
                `inv_id` = ? AND `item_id` = ? AND `owner_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["current_status_qty"]))
        inputs.append(inv_id)

        form_data = dict(request.form)

        # item_id
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        inputs.append(item_id)

        # owner_id
        inputs.append(form_data["owner_id"])

        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def remove_theoretic_inventory(mariadb_connection, inv_id, request, custom_response):
    """
    Removes from theoretic inventory.

    Parameters:
        mariadb_connection (object): MariaDB Connection Object
        inv_id (int): Inventory ID
        request (object): Flask Request Object
        custom_response (object): Flask Response Object

    Returns:
        (bool): True if successful, False otherwise
        custom_response (object): Flask Response Object

    Upon Failure:
        Returns: False, custom_response
        updating the custom_response object with error message
    """

    try:
        base_query = '''
            UPDATE `Inventory`.`Inventory`
            SET
                `theoretical_inventory` = `theoretical_inventory` - ?
            WHERE
                `inv_id` = ? AND `item_id` = ? AND `owner_id` = ?
        '''
        inputs = []
        inputs.append(float(request.form["current_status_qty"]))
        inputs.append(inv_id)

        form_data = dict(request.form)

        # item_id
        item_id, item_id_dir, custom_response = get_item_id(
            mariadb_connection, request, custom_response)
        if not item_id:
            raise ValueError
        inputs.append(item_id)

        # owner_id
        inputs.append(form_data["owner_id"])

        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        return True, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response

def get_inventory_for_single_record(mariadb_connection, inv_id, custom_response):
    """
    Gets inventory for a single record.

    Parameters:
        mariadb_connection (object): MariaDB Connection Object
        inv_id (int): Inventory ID
        custom_response (object): Flask Response Object

    Returns:
        (list): Row of data from inv_id
            [
                inv_id,
                item_id,
                owner_id,
                is_component,
                is_product,
                actual_inventory,
                theoretical_inventory
            ]
        custom_response (object): Flask Response Object

    Upon Failure:
        Returns: None, custom_response
        updating the custom_response object with error message
    """

    try:
        # Build Query
        if inv_id:
            base_query = '''
                SELECT
                    `inv_id`,
                    `item_id`,
                    `owner_id`,
                    `is_component`,
                    `is_product`,
                    `actual_inventory`,
                    `theoretical_inventory`
                FROM `Inventory`.`Inventory`
                WHERE
                    `inv_id` = ?
                LIMIT 1
            '''

            cursor = mariadb_connection.cursor()
            cursor.execute(base_query, (inv_id,))
            result = cursor.fetchone()
            if not result:
                custom_response.insert_flash_message(
                    FlashMessage(
                        message=f"Inv_id: {inv_id} does not exist in Inventory Table",
                        message_type=MessageType.DANGER
                    )
                )
                return None, custom_response
            return result, custom_response
        custom_response.insert_flash_message(
            FlashMessage(
                message="Inv_id was not provided.",
                message_type=MessageType.DANGER
            )
        )
        return None, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return None, custom_response

def get_item_id(mariadb_connection, request, custom_response):
    """
    Gets the item_id from `Inventory`.`Item_id, Atempts to create
    a new item_id if one doesn't already exist in the table.

    Parameters:
        mariadb_connection (object): MariaDB connection object
        request (object): Flask Request Object
        custom_response (object): Custom Response Object

    Returns:
        item_id (int): the item id from component_id or product_id
        item_id_dir (str): directory name for saving files
        custom_response (object): Custom Response Object

    Upon Failure:
        Returns None, None custom_response
        updating custom_responce object with error messages
    """

    try:

        form_data = dict(request.form)

        if "component_id" in form_data.keys():
            id = form_data["component_id"]
            id_col = "component_id"
        elif "product_id" in form_data.keys():
            id = form_data["product_id"]
            id_col = "product_id"
        else:
            custom_response.insert_form_message(
                form_id=0,
                message=Message(
                    message="Invalid item_id Key",
                    message_detail="Key must be component_id or product_id",
                    message_type=MessageType.DANGER
                )
            )
            return None, None, custom_response

        # Build Query
        base_query = """
        SELECT
            `item_id`
        FROM
            `Inventory`.`Item_id`
        """

        base_query += "WHERE `" + id_col + "` = ? LIMIT 1"

        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, (id, ))
        result = cursor.fetchone()

        if result:
            id_dir = id_col + "-" + str(id) + "__item_id-" + str(result[0])
            return result[0], id_dir, custom_response

        # Insert and get a new item_id if one doesn't exist
        insert_query = """
            INSERT INTO `Inventory`.`Item_id` (
                `product_id`,
                `component_id`
            )
            VALUES (
                ?, ?
            )
        """
        inputs = []
        if "component_id" in form_data.keys():
            inputs.append(None)
            inputs.append(id)
        else:
            inputs.append(id)
            inputs.append(None)

        cursor.execute(insert_query, tuple(inputs))
        item_id = cursor.lastrowid

        if item_id:
            id_dir = id_col + "-" + str(id) + "__item_id-" + str(item_id)
            mariadb_connection.commit()
            return item_id, id_dir, custom_response
        else:
            message = FlashMessage(
                message="Failed to fetch/create item_id",
                message_type=MessageType.DANGER
            )
            mariadb_connection.rollback()
            custom_response.insert_flash_message(message)
            return None, None, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        mariadb_connection.rollback()
        return None, None, custom_response

def check_facility_id_related_org_id(org_id, facility_id, custom_response):
    """
    Checks if the facility id exists in 
    `Organizations`.`Facilities` and also checks
    if the org_id and the facility_id are related
    in the `Organizations`.`Facilities` table.

    Parameters:
        org_id (int): organization_id
        facility_id (int): facility_id
        custom_response (object): Custom Response Object

    Returns:
        valid (bool): true if valid, false if not
        custom_response

    Upon Failure:
        Returns False, custom_response
        updating custom_response with error message
    """

    ### Connect to MariaDB ###
    try:
        # Test DB Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )

        base_query = """
            SELECT
                a.`organization_id`,
                a.`facility_id`,
                b.`courier`
            FROM
                `Organizations`.`Facilities` a
            JOIN `Organizations`.`Organizations` b ON
                a.`organization_id` = b.`organization_id`
            WHERE
                a.`organization_id` = ? AND
                a.`facility_id` = ?
            LIMIT 1
        """

        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, (org_id, facility_id))
        result = cursor.fetchone()

        if not result:
            custom_response.insert_form_message(
                form_id=4,
                message=Message(
                    message="Invalid facility_id",
                    message_detail="facility_id is not related to courier_id",
                    message_type=MessageType.DANGER
                )
            )
            return False, custom_response
        if not result[2]:
            custom_response.insert_form_message(
                form_id=4,
                message=Message(
                    message="Invalid courier_id",
                    message_detail="organization is not a courier",
                    message_type=MessageType.DANGER
                )
            )
            return False, custom_response
        return True, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return False, custom_response
