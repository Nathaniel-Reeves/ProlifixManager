'''
Handle Inventory Data
'''
import json
from sqlalchemy import select, text

from view.response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
import model as db
from model.connector import get_session
from .package import package_data

def get_components(custom_response,
        component_ids,
        component_types,
        certifications,
        brand_ids,
        populate,
        doc
    ):
    
    # Build the query
    tables = [db.Components, db.Component_Names]
    
    if 'product-materials' in populate:
        tables.append(db.Materials)
    if 'purchase-order-detail' in populate:
        tables.append(db.Purchase_Order_Detail)
    if 'label-formula-master' in populate:
        tables.append(db.Formula_Master)
    if 'ingredient-formula-detail' in populate:
        tables.append(db.Formula_Detail)
    if 'item-id' in populate or 'inventory' in populate:
        tables.append(db.Item_id)
    if 'inventory' in populate:
        tables.append(db.Inventory)
    if 'brand' in populate:
        tables.append(db.Organizations)
        tables.append(db.Organization_Names)
        
    stm = select(*tables) \
        .join(db.Component_Names, isouter=True)
    
    if 'product-materials' in populate:
        stm = stm.join(db.Materials, db.Components.component_id == db.Materials.component_id, isouter=True)
    if 'purchase-order-detail' in populate:
        stm = stm.join(db.Purchase_Order_Detail, db.Components.component_id == db.Purchase_Order_Detail.component_id, isouter=True)
    if 'label-formula-master' in populate:
        stm = stm.join(db.Formula_Master, db.Components.component_id == db.Formula_Master.label_id, isouter=True)
    if 'ingredient-formula-detail' in populate:
        stm = stm.join(db.Formula_Detail, db.Components.component_id == db.Formula_Detail.ingredient_id, isouter=True)
    if 'item-id' in populate or 'inventory' in populate:
        stm = stm.join(db.Item_id, db.Components.component_id == db.Item_id.component_id, isouter=True)
    if 'inventory' in populate:
        stm = stm.join(db.Inventory, db.Item_id.item_id == db.Inventory.item_id, isouter=True)
    if 'brand' in populate:
        stm = stm.join(db.Organizations, db.Components.brand_id == db.Organizations.organization_id, isouter=True)
        stm = stm.join(db.Organization_Names, db.Organizations.organization_id == db.Organization_Names.organization_id, isouter=True)
        
    stm = stm.where(db.Component_Names.primary_name == True)
    
    if 'brand' in populate:
        stm = stm.where(db.Organization_Names.primary_name == True)
    
    if component_ids:
        stm = stm.where(db.Components.component_id.in_(component_ids))
        
    if brand_ids:
        stm = stm.where(db.Components.brand_id.in_(brand_ids))
    
    if component_types:
        stm = stm.where(db.Components.component_type.in_(component_types))
        
    if certifications:
        if 'usda-organic' in certifications:
            stm = stm.where(db.Components.certified_usda_organic == True)
        if 'halal' in certifications:
            stm = stm.where(db.Components.certified_halal == True)
        if 'kosher' in certifications:
            stm = stm.where(db.Components.certified_kosher == True)
        if 'gluten-free' in certifications:
            stm = stm.where(db.Components.certified_gluten_free == True)
        if 'national-sanitation-foundation' in certifications:
            stm = stm.where(db.Components.certified_national_sanitation_foundation == True)
        if 'us-pharmocopeia' in certifications:
            stm = stm.where(db.Components.certified_us_pharmocopeia == True)
        if 'non-gmo' in certifications:
            stm = stm.where(db.Components.certified_non_gmo == True)
        if 'vegan' in certifications:
            stm = stm.where(db.Components.certified_vegan == True)
    
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