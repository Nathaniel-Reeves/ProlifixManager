'''
Handle Organizations Data
'''
from model.connector import get_session
import model as db
from sqlalchemy import select
from view.response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
from flask import (
    jsonify
)
def get_organizations(custom_response, org_ids, org_type, populate):
    """
    Fetch Organizaiton from the database.
    Populate them and filter them if requested.
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
        tables.append(db.Inventory_Components)
    if 'products' in populate:
        tables.append(db.Product_Master)

    stm = select(*tables)\
        .join(db.Organization_Names)
    
    def handle_join_error():
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response
            
    if 'facilities' in populate:
        try:
            stm.join(db.Facilities)
        except Exception:
            return handle_join_error()
    if 'sales-orders' in populate:
        try:
            stm.join(db.Sales_Orders)
        except Exception:
            return handle_join_error()
    if 'purchase-orders' in populate:
        try:
            stm.join(db.Purchase_Orders)
        except Exception:
            return handle_join_error()
    if 'people' in populate:
        try:
            stm.join(db.People)
        except Exception:
            return handle_join_error()
    if 'components' in populate:
        try:
            stm.join(db.Inventory_Components)
        except Exception:
            return handle_join_error()
    if 'products' in populate:
        try:
            stm.join(db.Product_Master)
        except Exception:
            return handle_join_error()
        
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
    data = {}
    for row in raw_data:
        table_obj = list(row)
        parent_key = table_obj[0].get_id()
        data[parent_key] = table_obj[0].to_dict()
        table_obj.pop(0)
        
        if table_obj:
            for table in table_obj:
                data[parent_key][table.__tablename__] = table.to_dict()
    custom_response.insert_data(data)
    return custom_response
    
    