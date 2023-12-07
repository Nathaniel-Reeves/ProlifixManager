'''
Handle Organizations Data
'''
import json
from sqlalchemy import select, text

from server.view import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
import model as db
from model.connector import get_session
from .package import package_data

def get_organizations(custom_response, org_ids, org_type, populate, doc):
    """
    Fetch Organizaiton from the database.
    Populate them and filter them if requested.
    
    Args:
        custom_response (CustomResponse): CustomResponse object
        org_ids (list): List of organization ids
        org_type (list): Organization types (enum)
            ('supplier', 'client', 'courier', 'lab')
            Note: an empty list will return all organizations
        populate (list): List of tables to populate (enum)
            ('facilities','sales-orders', 'purchase-orders', 'people', 'components', 'products')
        doc (bool): Whether or not to include the document column in the response
        
    Returns:
        custom_response (CustomResponse): CustomResponse object containing the data and relivant error messages.
    """
    
    # Build the query
    tables = [db.Organizations, db.Organization_Names]
    
    if 'facilities' in populate:
        tables.append(db.Facilities)
    if 'sales-orders' in populate:
        tables.append(db.Sales_Orders)
    if 'purchase-orders' in populate:
        tables.append(db.Purchase_Orders)
    if 'people' in populate:
        tables.append(db.People)
    if 'components' in populate:
        tables.append(db.Components)
    if 'products' in populate:
        tables.append(db.Product_Master)

    stm = select(*tables)\
          .join(db.Organization_Names, isouter=True)
            
    if 'facilities' in populate:
        stm = stm.join(db.Facilities, db.Organizations.organization_id == db.Facilities.organization_id, isouter=True)
    if 'sales-orders' in populate:
        stm = stm.join(db.Sales_Orders, db.Organizations.organization_id == db.Sales_Orders.organization_id, isouter=True)
    if 'purchase-orders' in populate:
        stm = stm.join(db.Purchase_Orders, db.Organizations.organization_id == db.Purchase_Orders.organization_id, isouter=True)
    if 'people' in populate:
        stm = stm.join(db.People, db.Organizations.organization_id == db.People.organization_id, isouter=True)
    if 'components' in populate:
        stm = stm.join(db.Components, db.Organizations.organization_id == db.Components.brand_id, isouter=True)
    if 'products' in populate:
        stm = stm.join(db.Product_Master, db.Organizations.organization_id == db.Product_Master.organization_id, isouter=True)
        
    stm = stm.where(db.Organization_Names.primary_name == True)
    
    if org_type:
        if 'client' in org_type:
            stm = stm.where(db.Organizations.client == True)
        if 'supplier' in org_type:
            stm = stm.where(db.Organizations.supplier == True)
        if 'lab' in org_type:
            stm = stm.where(db.Organizations.lab == True)
        if 'courier' in org_type:
            stm = stm.where(db.Organizations.courier == True)
    
    if org_ids:
        stm = stm.where(db.Organizations.organization_id.in_(org_ids))
            
    # Connect to the database
    try:
        session = get_session()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response
        
    # Execute the query
    try:
        stream = session.execute(stm)
        raw_data = stream.all()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response
    
    session.close()
    
    # Process and Package the data
    data, custom_response = package_data(raw_data, doc, custom_response)
    custom_response.insert_data(data)
    return custom_response

def organization_exists(names, custom_response):
    """
    Check if an organization already exists by organization name.
    """
    # Execute Querys
    primary_exists = False
    levenshtein_results = []
    for name in names:
        if name["primary_name"]:
            primary_exists = True
        results, levensthein_messages = check_org_exists_levenshtein(
            name["organization_name"])
        if not results == -1:
            levenshtein_results += results
        custom_response.insert_flash_messages(levensthein_messages)

    # Handle Primary False
    if not primary_exists:
        e_message = FlashMessage(
            message="Primary Name not selected!",
            message_type=MessageType.WARNING)
        custom_response.insert_flash_message(e_message)

    # Insert the levenshtein_results into the response
    custom_response.insert_data(levenshtein_results)

    return custom_response


def check_org_exists_levenshtein(search_name):
    '''
    Checks likelyhood if Organization Name already exists
    in the Database.
    '''
    try:
        session = get_session()

        # Build Query
        base_query = """
        SELECT
            JSON_OBJECT(
                'organization_id', `organization_id`,
                'organization_name', `organization_name`,
                'levenshtein_probability', CAST(sys.LEVENSHTEIN_RATIO(`organization_name`, :search_name) AS UNSIGNED INTEGER)
            ) AS levenshtein_results
        FROM `Organizations`.`Organization_Names`
        WHERE
            sys.LEVENSHTEIN_RATIO(`organization_name`, :search_name) > 50;
        """

        # Execute Query
        result = session.execute(
            text(base_query), 
            {"search_name":search_name}
        )
        print(result)

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
        error = error_message()
        return -1, [error]
