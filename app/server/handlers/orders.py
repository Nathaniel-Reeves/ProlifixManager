'''
Handle Orders Data
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
    CustomResponse
)

bp = Blueprint('orders', __name__, url_prefix='/orders')

@bp.route('/', methods=['GET'])
@check_authenticated(authentication_required=True)
def get_lot_numbers():
    '''
    Get all Lot Numbers
    '''

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
                'product_name', b.`product_name`,
                'organization_id', b.`organization_id`
            )
        AS lot_number_objects
        FROM `Orders`.`Lot_Numbers` a
        LEFT JOIN `Products`.`Product_Master` b ON 
            a.`product_id` = b.`product_id`
        '''

        # Build Query
        lot_numbers = request.args.getlist('lot-numbers')
        org_ids = request.args.getlist('org-ids')
        inputs = None
        if lot_numbers or org_ids:
            where_clause = 'WHERE '
            if lot_numbers:
                where_clause += f"""
                    a.`prolifix_lot_number` IN ({", ".join(["?"] * len(lot_numbers))})
                """
                inputs = tuple(lot_numbers)
                if org_ids:
                    where_clause += f"""
                        AND
                        b.`organization_id` IN ({", ".join(["?"] * len(org_ids))})
                    """
                    inputs = tuple(lot_numbers + org_ids)
            elif org_ids:
                where_clause += f"""b.`organization_id` IN ({", ".join(["?"] * len(org_ids))})"""
                inputs = tuple(org_ids)
            base_query += where_clause

        order_by = """
        ORDER BY 
            a.`year` DESC, 
            a.`month` DESC, 
            a.`sec_number` DESC;
        """
        print(inputs)

        base_query += order_by
        print(base_query)

        # Execute Query
        cursor = mariadb_connection.cursor()
        cursor.execute(base_query, inputs)
        result = cursor.fetchall()

        # Return JSON
        orders = []
        for row in result:
            json_row = json.loads(row[0])
            orders.append(json_row)

        custom_response.insert_data(orders)

        return jsonify(custom_response.to_json())

    except mariadb.Error as error:
        custom_response.insert_flash_message(FlashMessage(
            message=str(error), message_type=MessageType.DANGER))
        return jsonify(custom_response.to_json()), 500

    finally:
        if 'mariadb_connection' in locals():
            mariadb_connection.close()
