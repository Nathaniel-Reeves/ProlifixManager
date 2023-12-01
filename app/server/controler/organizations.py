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
def get_organizations(custom_response, org_ids, org_type, populate, doc):
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
    
    
def package_data(raw_data, doc, custom_response):
    try:
        data = {}
        for i, row in enumerate(raw_data):
            parent_key = row[0].get_id()
            
            if i == 0 or parent_key != raw_data[i - 1][0].get_id():
                d = row[0].to_dict()
                if not doc and ("doc" in list(d.keys())):
                    d["doc"] = {}
                data[parent_key] = d
            
            
            if len(row) > 1:
                for j, table in enumerate(row, 0):
                    if j == 0:
                        continue
                    if table == None:
                        continue

                    if table.__tablename__ not in data[parent_key]:
                        data[parent_key][table.__tablename__] = []
                        

                    entered_keys = []
                    for d in data[parent_key][table.__tablename__]:
                        if isinstance(table.get_id(), int):
                            entered_keys.append(d[table.get_id_name()])
                        else:
                            entered_keys.append((
                                d["prefix"],
                                d["year"],
                                d["month"],
                                d["sec_number"],
                                d["suffix"]
                            ))
                            
                    if table.get_id() not in entered_keys:
                        d = table.to_dict()
                        if not doc and ("doc" in list(d.keys())):
                            d["doc"] = {}
                        data[parent_key][table.__tablename__].append(d)
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
    return data, custom_response