'''
Handle Organizations Data
'''
import os
import json
import mariadb
from flask import (
    Blueprint,
    request,
    jsonify
)

HOST = os.environ.get('DB_HOSTNAME')
PORT = os.environ.get('DB_PORT')
USER = os.environ.get('DB_USERNAME')
PASSWORD = os.environ.get('DB_PASSWORD')

bp = Blueprint('organizations', __name__, url_prefix='/organizations')


@bp.route('/', methods=['GET'])
def get_organizations():
    '''
    Get all organizations
    '''
    try:
        # Test Connection
        session = mariadb.connect(
            host=HOST,
            port=int(PORT),
            user=USER,
            password=PASSWORD
        )

        # Build Query
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
                'other', a.`other`,
                'doc', a.`doc`,
                'notes', a.`notes`,
                'organization_name', b.`organization_name`
            )
        AS organization_objects
        FROM `Organizations`.`Organizations` a
        LEFT JOIN `Organizations`.`Organization_Names` b ON 
            a.`organization_id` = b.`organization_id`
        WHERE b.`primary_name` = true
        '''
        org_id = request.args.get(
            'org-id', default=None, type=int)
        if org_id:
            base_query += f' AND a.`organization_id` = {org_id}'

        org_type = request.args.getlist('org-type')
        if 'client' in org_type:
            base_query += ' AND a.`client` = 1'
        if 'supplier' in org_type:
            base_query += ' AND a.`supplier` = 1'
        if 'lab' in org_type:
            base_query += ' AND a.`lab` = 1'

        populate = request.args.getlist('populate')

        # Execute Query
        cursor = session.cursor()
        cursor.execute(base_query)
        result = cursor.fetchall()

        # Return JSON
        organizations = {}
        for row in result:
            json_row = json.loads(row[0])
            org_id = json_row['organization_id']
            organizations[org_id] = json_row

            # Populate child resources
            if 'facilities' in populate:
                facilities = populate_facilities(cursor, org_id)
                if isinstance(facilities, (dict,)):
                    organizations[org_id]['facilities'] = facilities
                else:
                    return jsonify(error=str(facilities))

            if 'sales-orders' in populate:
                sales_orders = populate_sales_orders(cursor, org_id)
                if isinstance(sales_orders, (dict,)):
                    organizations[org_id]['sales_orders'] = sales_orders
                else:
                    return jsonify(error=str(sales_orders))

            if 'purchase-orders' in populate:
                purchase_orders = populate_purchase_orders(cursor, org_id)
                if isinstance(purchase_orders, (dict,)):
                    organizations[org_id]['purchase_orders'] = purchase_orders
                else:
                    return jsonify(error=str(purchase_orders))

            if 'people' in populate:
                people = populate_people(cursor, org_id)
                if isinstance(people, (dict,)):
                    organizations[org_id]['people'] = people
                else:
                    return jsonify(error=str(people))

            if 'components' in populate:
                components = populate_components(cursor, org_id)
                if isinstance(components, (dict,)):
                    organizations[org_id]['components'] = components
                else:
                    return jsonify(error=str(components))

            if 'products' in populate:
                products = populate_products(cursor, org_id)
                if isinstance(products, (dict,)):
                    organizations[org_id]['products'] = products
                else:
                    return jsonify(error=str(products))

        return jsonify(organizations)

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return jsonify(error=str(error))

    finally:
        if 'session' in locals():
            session.close()

def populate_facilities(cursor, org_id):
    '''
    Populate Organization with Facilities

    Attributes:
        cursor (MariaDB.cursor): Database cursor
        org_id (int): Organization ID

    Returns:
        facilities (dict): Dict of facilities

    Raises:
        MariaDB.Error: Database error
    '''

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

    try:
        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return error

    # Return Facilities Dictionary
    facilites = {}
    for row in result:
        json_row = json.loads(row[0])
        facility_id = json_row['facility_id']
        facilites[facility_id] = json_row
    return facilites

def populate_sales_orders(cursor, org_id):
    '''
    Populate Organization with Sales Orders

    Attributes:
        cursor (MariaDB.cursor): Database cursor
        org_id (int): Organization ID

    Returns:
        sales_orders (dict): Dict of Sales Orders

    Raises:
        MariaDB.Error: Database error
    '''

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

    try:
        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return error

    # Return Facilities Dictionary
    sales_orders = {}
    for row in result:
        json_row = json.loads(row[0])
        sales_order_id = "SO#" + \
                        str(json_row['prefix']) + \
                        str(json_row['year']) + \
                        str(json_row['month']) + \
                        str(json_row['sec_number'])
        sales_orders[sales_order_id] = json_row
    return sales_orders

def populate_purchase_orders(cursor, org_id):
    '''
    Populate Organization with Purchase Orders

    Attributes:
        cursor (MariaDB.cursor): Database cursor
        org_id (int): Organization ID

    Returns:
        purchase_orders (dict): Dict of Purchase Orders

    Raises:
        MariaDB.Error: Database error
    '''

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

    try:
        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return error

    # Return Facilities Dictionary
    purchase_orders = {}
    for row in result:
        json_row = json.loads(row[0])
        purchase_order_id = "PO#" + \
            str(json_row['prefix']) + \
            str(json_row['year']) + \
            str(json_row['month']) + \
            str(json_row['sec_number'])
        purchase_orders[purchase_order_id] = json_row
    return purchase_orders

def populate_people(cursor, org_id):
    '''
    Populate Organization with People

    Attributes:
        cursor (MariaDB.cursor): Database cursor
        org_id (int): Organization ID

    Returns:
        people (dict): Dict of People

    Raises:
        MariaDB.Error: Database error
    '''

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

    try:
        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return error

    # Return Facilities Dictionary
    people = {}
    for row in result:
        json_row = json.loads(row[0])
        person_id = json_row['person_id']
        people[person_id] = json_row
    return people

def populate_components(cursor, org_id):
    '''
    Populate Organization with Components

    Attributes:
        cursor (MariaDB.cursor): Database cursor
        org_id (int): Organization ID

    Returns:
        components (dict): Dict of Components

    Raises:
        MariaDB.Error: Database error
    '''

    query = '''
    SELECT 
        JSON_OBJECT(
            'component_id', a.`component_id`,
            'component_type', a.`component_type`,
            'owner_id', a.`owner_id`,
            'doc', a.`doc`,
            'component_name', b.`component_name`
        )
    AS components_objects
    FROM `Inventory`.`Components` a 
    LEFT JOIN `Inventory`.`Component_Names` b ON
        a.`component_id` = b.`component_id` 
    WHERE 
        a.`owner_id` = ? AND 
        b.`primary_name` = 1
    '''

    try:
        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return error

    # Return Facilities Dictionary
    components = {}
    for row in result:
        json_row = json.loads(row[0])
        component_id = json_row['component_id']
        components[component_id] = json_row
    return components

def populate_products(cursor, org_id):
    '''
    Populate Organization with Products

    Attributes:
        cursor (MariaDB.cursor): Database cursor
        org_id (int): Organization ID

    Returns:
        products (dict): Dict of Products

    Raises:
        MariaDB.Error: Database error
    '''

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

    try:
        # Execute Query
        cursor.execute(query, (org_id,))
        result = cursor.fetchall()

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return error

    # Return Facilities Dictionary
    products = {}
    for row in result:
        json_row = json.loads(row[0])
        product_id = json_row['product_id']
        products[product_id] = json_row
    return products
