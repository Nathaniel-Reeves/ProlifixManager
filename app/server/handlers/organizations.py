'''
Handle Organizations Data
'''
import json
import mariadb
from flask import (
    Blueprint,
    request,
    jsonify,
    current_app as app
)
from .auth import check_authenticated
from .response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
from .helper import (
    only_integers
)

bp = Blueprint('organizations', __name__, url_prefix='/organizations')

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def get_organizations():
    """
    Fetch Organizaiton from the database.
    Populate them and filter them if requested.
    """

    try:
        custom_response = CustomResponse()  # Create an instance of Response

        # Test Connection
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
                AS organization_objects
                FROM `Organizations`.`Organizations` a
                LEFT JOIN `Organizations`.`Organization_Names` b ON 
                    a.`organization_id` = b.`organization_id`
                WHERE b.`primary_name` = true
            '''
        else:
            base_query = '''
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
                        'doc', a.`doc`,
                        'notes', a.`notes`,
                        'organization_name', b.`organization_name`,
                        'organization_initial', b.`organization_initial`
                    )
                AS organization_objects
                FROM `Organizations`.`Organizations` a
                LEFT JOIN `Organizations`.`Organization_Names` b ON 
                    a.`organization_id` = b.`organization_id`
                WHERE b.`primary_name` = true
            '''

        inputs = []

        org_ids = request.args.getlist('org-id')
        if org_ids:
            cleaned_org_ids = list(only_integers(org_ids))
            base_query += f''' AND a.`organization_id` IN ({", ".join(["?"] * len(cleaned_org_ids))})'''
            inputs += cleaned_org_ids

        org_type = request.args.getlist('org-type')
        if 'client' in org_type:
            base_query += ' AND a.`client` = 1'
        if 'supplier' in org_type:
            base_query += ' AND a.`supplier` = 1'
        if 'lab' in org_type:
            base_query += ' AND a.`lab` = 1'
        if 'courier' in org_type:
            base_query += ' AND a.`courier` = 1'

        verbose = request.args.get("verbose", type=bool, default=False)

        populate = request.args.getlist('populate')

        # Execute Query
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, tuple(inputs))
        result = cursor.fetchall()

        if not result:
            custom_response.insert_flash_message(FlashMessage(
                message='No organizations found',
                message_type=MessageType.WARNING))
            return jsonify(custom_response.to_json()), 404

        # Process Organizations
        organizations = {}
        for row in result:
            json_row = json.loads(row[0])
            org_id = json_row['organization_id']
            organizations[org_id] = json_row

            # Populate child resources
            if 'facilities' in populate:
                organizations, custom_response = populate_facilities(
                                                 cursor, org_id,
                                                 organizations, custom_response, verbose)

            if 'sales-orders' in populate:
                organizations, custom_response = populate_sales_orders(
                                                 cursor, org_id,
                                                 organizations,
                                                 custom_response, verbose)

            if 'purchase-orders' in populate:
                organizations, custom_response = populate_purchase_orders(
                                                 cursor, org_id,
                                                 organizations,
                                                 custom_response, verbose)

            if 'people' in populate:
                organizations, custom_response = populate_people(
                                                 cursor, org_id,
                                                 organizations,
                                                 custom_response, verbose)

            if 'components' in populate:
                organizations, custom_response = populate_components(
                                                 cursor, org_id,
                                                 organizations,
                                                 custom_response, verbose)

            if 'products' in populate:
                organizations, custom_response = populate_products(
                                                 cursor, org_id,
                                                 organizations,
                                                 custom_response, verbose)

        # Insert the processed organizations into the response
        custom_response.insert_data(organizations)

        return jsonify(custom_response.to_json()), 200

    except Exception:
        error = error_message()
        custom_response.insert_flashMessage(error)
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()

def populate_facilities(cursor, org_id, organizations,
                        custom_response, verbose):
    '''
    Populate Facilities Resource for Organizations

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        org_id (int): Organization ID
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'facility_id', a.`facility_id`,
                'building_name', a.`building_name`,
                'building_type', a.`building_type`,
                'street_1_number', a.`street_1_number`,
                'street_1_number_suffix', a.`street_1_number_suffix`,
                'street_1_name', a.`street_1_name`,
                'street_1_type', a.`street_1_type`,
                'street_1_direction', a.`street_1_direction`,
                'street_2_number', a.`street_2_number`,
                'street_2_number_suffix', a.`street_2_number_suffix`,
                'street_2_name', a.`street_2_name`,
                'street_2_type', a.`street_2_type`,
                'street_2_direction', a.`street_2_direction`,
                'address_type', a.`address_type`,
                'address_type_identifier', a.`address_type_identifier`,
                'local_municipality', a.`local_municipality`,
                'city_town', a.`city_town`,
                'governing_district', a.`governing_district`,
                'postal_area', a.`postal_area`,
                'country', a.`country`,
                'ship_time', a.`ship_time`,
                'ship_time_units', a.`ship_time_units`,
                'ship_time_in_days', a.`ship_time_in_days`,
                'notes', a.`notes`
            )
        AS facility_objects
        FROM `Organizations`.`Facilities` a 
        WHERE a.`organization_id` = ?
        '''

        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

        # Create Facilities Dictionary
        facilites = {}
        for row in result:
            json_row = json.loads(row[0])
            facility_id = json_row['facility_id']
            facilites[facility_id] = json_row

        organizations[org_id]['facilities'] = facilites

        # If facility resource is empty
        if not facilites and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No facilities found for organization {organizations[org_id]["organization_name"]} (ID: {org_id})',
                    message_type=MessageType.WARNING)
            )

        return organizations, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return organizations, custom_response


def populate_sales_orders(cursor, org_id, organizations,
                          custom_response, verbose):
    '''
    Populate Sales Orders Resource for Organizations

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        org_id (int): Organization ID
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'prefix', a.`prefix`,
                'year', a.`year`,
                'month', a.`month`,
                'sec_number', a.`sec_number`,
                'organization_id', a.`organization_id`,
                'client_po_num', a.`client_po_num`,
                'order_date', a.`order_date`,
                'target_completion_date', a.`target_completion_date`,
                'completion_date', a.`completion_date`,
                'date_entered', a.`date_entered`,
                'doc', a.`doc`
            )
        AS sales_order_objects
        FROM `Orders`.`Sales_Orders` a 
        WHERE a.`organization_id` = ?
        '''

        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

        # Create Sales Order Dictionary
        sales_orders = {}
        for row in result:
            json_row = json.loads(row[0])
            sales_order_id = "SO#" + \
                str(json_row['prefix']) + \
                str(json_row['year']) + \
                str(json_row['month']) + \
                str(json_row['sec_number'])
            sales_orders[sales_order_id] = json_row

        organizations[org_id]['sales_orders'] = sales_orders

        # If sales order resource is empty
        if not sales_orders and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No sales orders found for organization {organizations[org_id]["organization_name"]} (ID: {org_id})',
                    message_type=MessageType.WARNING)
            )

        return organizations, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return organizations, custom_response


def populate_purchase_orders(cursor, org_id, organizations,
                             custom_response, verbose):
    '''
    Populate Purchase Orders Resource for Organizations

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        org_id (int): Organization ID
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'prefix', a.`prefix`,
                'year', a.`year`,
                'month', a.`month`,
                'sec_number', a.`sec_number`,
                'organization_id', a.`organization_id`,
                'supplier_so_num', a.`supplier_so_num`,
                'order_date', a.`order_date`,
                'eta_date', a.`eta_date`,
                'date_entered', a.`date_entered`,
                'doc', a.`doc`
            )
        AS purchase_order_objects
        FROM `Orders`.`Purchase_Orders` a 
        WHERE a.`organization_id` = ?
        '''

        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

        # Create Purchase Order Dictionary
        purchase_orders = {}
        for row in result:
            json_row = json.loads(row[0])
            purchase_order_id = "PO#" + \
                str(json_row['prefix']) + \
                str(json_row['year']) + \
                str(json_row['month']) + \
                str(json_row['sec_number'])
            purchase_orders[purchase_order_id] = json_row

        organizations[org_id]['purchase_orders'] = purchase_orders

        # If purchase order resource is empty
        if not purchase_orders and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No purchase orders found for organization {organizations[org_id]["organization_name"]} (ID: {org_id})',
                    message_type=MessageType.WARNING)
            )

        return organizations, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return organizations, custom_response


def populate_people(cursor, org_id, organizations,
                    custom_response, verbose):
    '''
    Populate People Resource for Organizations

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        org_id (int): Organization ID
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'person_id', a.`person_id`,
                'first_name', a.`first_name`,
                'last_name', a.`last_name`,
                'date_entered', a.`date_entered`,
                'job_description', a.`job_description`,
                'department', a.`department`,
                'phone_number_primary', a.`phone_number_primary`,
                'phone_number_secondary', a.`phone_number_secondary`,
                'email_address_primary', a.`email_address_primary`,
                'email_address_secondary', a.`email_address_secondary`,
                'birthday', a.`birthday`,
                'is_employee', a.`is_employee`,
                'contract_date', a.`contract_date`,
                'termination_date', a.`termination_date`,
                'clock_number', a.`clock_number`
            )
        AS people_objects
        FROM `Organizations`.`People` a 
        WHERE a.`organization_id` = ?
        '''

        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

        # Create People Dictionary
        people = {}
        for row in result:
            json_row = json.loads(row[0])
            person_id = json_row['person_id']
            people[person_id] = json_row

        organizations[org_id]['people'] = people

        # If people resource is empty
        if not people and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No people found for organization {organizations[org_id]["organization_name"]} (ID: {org_id})',
                    message_type=MessageType.WARNING)
            )

        return organizations, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return organizations, custom_response


def populate_components(cursor, org_id, organizations,
                        custom_response, verbose):
    '''
    Populate Components Resource for Organizations

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        org_id (int): Organization ID
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'component_id', a.`component_id`,
                'brand_id', a.`brand_id`,
                'component_type', a.`component_type`,
                'units', a.`units`,
                'date_entered', a.`date_entered`,
                'doc', a.`doc`,
                'component_name', b.`component_name`,
                'certified_usda_organic', a.`certified_usda_organic`,
                'certified_halal', a.`certified_halal`,
                'certified_kosher', a.`certified_kosher`,
                'certified_gluten_free', a.`certified_gluten_free`,
                'certified_national_sanitation_foundation', a.`certified_national_sanitation_foundation`,
                'certified_us_pharmacopeia', a.`certified_us_pharmacopeia`,
                'certified_non_gmo', a.`certified_non_gmo`,
                'certified_vegan', a.`certified_vegan`
            )
        AS components_objects
        FROM `Inventory`.`Components` a 
        LEFT JOIN `Inventory`.`Component_Names` b ON
            a.`component_id` = b.`component_id` 
        WHERE 
            a.`brand_id` = ? AND 
            b.`primary_name` = 1
        '''

        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

        # Create Components Dictionary
        components = {}
        for row in result:
            json_row = json.loads(row[0])
            component_id = json_row['component_id']
            components[component_id] = json_row

        organizations[org_id]['components'] = components

        # If components resource is empty
        if not components and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No components found for organization {organizations[org_id]["organization_name"]} (ID: {org_id})',
                    message_type=MessageType.WARNING)
            )

        return organizations, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return organizations, custom_response


def populate_products(cursor, org_id, organizations,
                      custom_response, verbose):
    '''
    Populate Products for Organizations

    Args:
        cursor (mariadb.cursor): MariaDB Cursor
        org_id (int): Organization ID
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
        verbose (bool): Verbose

    Returns:
        organization (dict): Organizations Dictionary
        custom_response (CustomResponse): Custom Response
    '''

    try:
        query = '''
        SELECT 
            JSON_OBJECT(
                'product_id', a.`product_id`,
                'organization_id', a.`organization_id`,
                'product_name', a.`product_name`,
                'type', a.`type`,
                'current_product', a.`current_product`,
                'date_entered', a.`date_entered`,
                'spec_issue_date', a.`spec_issue_date`,
                'spec_revise_date', a.`spec_revise_date`,
                'doc', a.`doc`,
                'exp_time_frame', a.`exp_time_frame`,
                'exp_unit', a.`exp_unit`,
                'exp_type', a.`exp_type`,
                'exp_use_oldest_ingredient', a.`exp_use_oldest_ingredient`,
                'default_formula_id', a.`default_formula_id`
            )
        AS products_objects
        FROM `Products`.`Product_Master` a 
        WHERE 
            a.`organization_id` = ?
        '''

        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

        # Create Products Dictionary
        products = {}
        for row in result:
            json_row = json.loads(row[0])
            product_id = json_row['product_id']
            products[product_id] = json_row

        organizations[org_id]['products'] = products

        # If products resource is empty
        if not products and verbose:
            custom_response.insert_flash_message(
                FlashMessage(
                    message=f'No products found for organization {organizations[org_id]["organization_name"]} (ID: {org_id})',
                    message_type=MessageType.WARNING)
            )

        return organizations, custom_response

    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        return organizations, custom_response


@bp.route('/exists', methods=['GET'])
@check_authenticated(authentication_required=True)
def organization_exists():
    """
    Check if an organization already exists by organization name.
    """
    custom_response = CustomResponse()  # Create an instance of Response

    names = request.json['names']

    # Execute Querys
    primary_exists = False
    levenshtein_results = []
    for name in names:
        if name["primary_name"]:
            primary_exists = True
        results, levensthein_messages = check_org_exists_levenshtein(
            name["organization_name"])
        if not isinstance(results, FlashMessage):
            levenshtein_results += results
        else:
            custom_response.insert_flash_message(results)
        custom_response.insert_flash_messages(levensthein_messages)

    # Handle Primary False
    if not primary_exists:
        e_message = FlashMessage(
            message="Primary Name not selected!",
            message_type=MessageType.WARNING)
        custom_response.insert_flash_message(e_message)

    # Insert the levenshtein_results into the response
    custom_response.insert_data(levenshtein_results)

    return jsonify(custom_response.to_json())


def check_org_exists_levenshtein(search_name):
    '''
    Checks likelyhood if Organization Name already exists
    in the Database.
    '''
    try:
        # Test Connection
        mariadb_connection = mariadb.connect(
            host=app.config['DB_HOSTNAME'],
            port=int(app.config['DB_PORT']),
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD']
        )
        cursor = mariadb_connection.cursor()

        # Build Query
        base_query = '''
        SELECT
            JSON_OBJECT(
                'organization_id', `organization_id`,
                'organization_name', `organization_name`,
                'levenshtein_probability', CAST(sys.LEVENSHTEIN_RATIO(`organization_name`, ?) AS UNSIGNED INTEGER)
            ) AS levenshtein_results
        FROM `Organizations`.`Organization_Names`
        WHERE
            sys.LEVENSHTEIN_RATIO(`organization_name`, ?) > 50;
        '''

        # Execute Query
        cursor.execute(base_query, (search_name, search_name))
        result = cursor.fetchall()

        # Return Results
        levensthein_results = []
        levensthein_messages = []
        for row in result:
            # Save Data
            json_row = json.loads(row[0])
            levensthein_results.append(json_row)

            # Create Message Components
            message_alert_heading = "Possible Duplicate Organization."
            message = f"Possible duplicate organization between '{search_name}' and '{json_row['organization_name']}'."
            message_detail = f"'{search_name}' is a {json_row['levenshtein_probability']} percent match for '{json_row['organization_name']}'.  Are they the same organization?"
            message_link = f"/api/organizations/?org-id={json_row['organization_id']}"

            # Create Message Object using Components
            message_obj = FlashMessage(
                alert_heading=message_alert_heading,
                message=message,
                message_detail=message_detail,
                link=message_link,
                message_type=MessageType.WARNING
            )
            levensthein_messages.append(message_obj)

        return levensthein_results, levensthein_messages

    except Exception:
        return error_message()
