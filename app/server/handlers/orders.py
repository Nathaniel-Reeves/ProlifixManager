'''
Handle Orders Data
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
if HOST is None:
    HOST = '127.0.0.1'

PORT = os.environ.get('DB_PORT')
if PORT is None:
    PORT = '3306'

USER = os.environ.get('DB_USERNAME')
if USER is None:
    USER = 'client'

PASSWORD = os.environ.get('DB_PASSWORD')
if PASSWORD is None:
    PASSWORD = "ClientPassword!5"
    
bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/lot-numbers', methods=['GET'])
def get_lot_numbers():
    '''
    Get all Lot Numbers
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
                'prefix', a.`prefix`, 
                'year', a.`year`,
                'month', a.`month`,
                'sec_number', a.`sec_number`,
                'suffix', a.`suffix`,
                'product_id', a.`product_id`,
                'prolifix_lot_number', a.`prolifix_lot_number`,
                'so_detail_id', a.`so_detail_id`,
                'target_unit_yield', a.`target_unit_yield`,
                'actual_unit_yield', a.`actual_unit_yield`,
                'retentions', a.`retentions`,
                'total_shippable_product', a.`total_shippable_product`,
                'doc', a.`doc`,
                'batch_printed', a.`batch_printed`,
                'bpr_printed', a.`bpr_printed`,
                'date_entered', a.`date_entered`,
                'exp_date', a.`exp_date`,
                'exp_type', a.`exp_type`,
                'product_name', b.`product_name`
            )
        AS lot_number_objects
        FROM `Orders`.`Lot_Numbers` a
        LEFT JOIN `Products`.`Product_Master` b ON 
            a.`product_id` = b.`product_id`
        ORDER BY 
            a.`year` DESC, 
            a.`month` DESC, 
            a.`sec_number` DESC;
        '''

        # Ececute Query
        cursor = session.cursor()
        cursor.execute(base_query)
        result = cursor.fetchall()

        # Return JSON
        orders = []
        for row in result:
            json_row = json.loads(row[0])
            orders.append(json_row)

        return jsonify(orders)

    except mariadb.Error as error:
        # Error Handling
        print(error)
        return jsonify(error=str(error))

    finally:
        if 'session' in locals():
            session.close()
