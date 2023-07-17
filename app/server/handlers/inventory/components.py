'''
Handle Component Functions
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

bp = Blueprint('components', __name__, url_prefix='/components')

def only_integers(iterable):
    '''
    Only accept integers
    '''
    for item in iterable:
        try:
            yield int(item)
        except ValueError:
            pass

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

        inputs = []

        org_ids = request.args.getlist('org-id')
        if org_ids:
            cleaned_org_ids = list(only_integers(org_ids))
            base_query += f''' AND a.`owner_id` IN ({", ".join(["?"] * len(cleaned_org_ids))})'''
            inputs += cleaned_org_ids

        component_ids = request.args.getlist('component-id')
        if component_ids:
            cleaned_component_ids = list(only_integers(component_ids))
            print(cleaned_component_ids)
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
                names = populate_component_names(cursor, component_id)
                if isinstance(names, list):
                    components[component_id]['names'] = names
                else:
                    custom_response.insert_flash_message(names)

        # Insert the processed component data into the response
        custom_response.insert_data(components)
        if components:
            return jsonify(custom_response.to_json()), 200
        else:
            return jsonify(custom_response.to_json()), 404

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

def populate_component_names(cursor, component_id):
    """
    Populates Component Objects with their
    alias names.

    Attributes:
        cursor (MaraDB.cursor): Database cursor
        component_id (int): Component Id

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

        return names

    except Exception as e:
        return error_message()
