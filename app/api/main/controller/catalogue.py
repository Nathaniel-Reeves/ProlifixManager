'''
Handle Inventory Data
'''
import json
from sqlalchemy import select, insert, text

from view.response import (
    MessageType,
    FlashMessage,
    CustomResponse,
    error_message
)
import model as db
from model.connector import get_session
from .package import package_data

def get_components(
        custom_response,
        component_ids,
        component_types,
        certifications,
        brand_ids,
        populate,
        doc
    ):
    
    # Build the query
    tables = [db.Components, db.Component_Names]
    
    if 'product_materials' in populate:
        tables.append(db.Materials)
    if 'purchase_order_detail' in populate:
        tables.append(db.Purchase_Order_Detail)
    if 'label_formula-master' in populate:
        tables.append(db.Formula_Master)
    if 'ingredient_formula_detail' in populate:
        tables.append(db.Formula_Detail)
    if 'item_id' in populate or 'inventory' in populate:
        tables.append(db.Item_id)
    if 'inventory' in populate:
        tables.append(db.Inventory)
    if 'brand' in populate:
        tables.append(db.Organizations)
        tables.append(db.Organization_Names)
        
    stm = select(*tables) \
        .join(db.Component_Names, isouter=True)
    
    if 'product_materials' in populate:
        stm = stm.join(db.Materials, db.Components.component_id == db.Materials.component_id, isouter=True)
    if 'purchase_order_detail' in populate:
        stm = stm.join(db.Purchase_Order_Detail, db.Components.component_id == db.Purchase_Order_Detail.component_id, isouter=True)
    if 'label_formula_master' in populate:
        stm = stm.join(db.Formula_Master, db.Components.component_id == db.Formula_Master.label_id, isouter=True)
    if 'ingredient-formula-detail' in populate:
        stm = stm.join(db.Formula_Detail, db.Components.component_id == db.Formula_Detail.ingredient_id, isouter=True)
    if 'item_id' in populate or 'inventory' in populate:
        stm = stm.join(db.Item_id, db.Components.component_id == db.Item_id.component_id, isouter=True)
    if 'inventory' in populate:
        stm = stm.join(db.Inventory, db.Item_id.item_id == db.Inventory.item_id, isouter=True)
    if 'brand' in populate:
        stm = stm.join(db.Organizations, db.Components.brand_id == db.Organizations.organization_id, isouter=True)
        stm = stm.join(db.Organization_Names, db.Organizations.organization_id == db.Organization_Names.organization_id, isouter=True)
        
    stm = stm.where(db.Component_Names.primary_name == True)
    
    if component_ids:
        stm = stm.where(db.Components.component_id.in_(component_ids))
        
    if brand_ids:
        stm = stm.where(db.Components.brand_id.in_(brand_ids))
    
    if component_types:
        stm = stm.where(db.Components.component_type.in_(component_types))
    
    if certifications:
        if 'usda_organic' in certifications:
            stm = stm.where(db.Components.certified_usda_organic == True)
        if 'halal' in certifications:
            stm = stm.where(db.Components.certified_halal == True)
        if 'kosher' in certifications:
            stm = stm.where(db.Components.certified_kosher == True)
        if 'gluten_free' in certifications:
            stm = stm.where(db.Components.certified_gluten_free == True)
        if 'national-sanitation-foundation' in certifications:
            stm = stm.where(db.Components.certified_national_sanitation_foundation == True)
        if 'us-pharmocopeia' in certifications:
            stm = stm.where(db.Components.certified_us_pharmacopeia == True)
        if 'non_gmo' in certifications:
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
        custom_response.set_status_code(400)
        return custom_response
    
    session.close()
    # Process and Package the data
    data, custom_response = package_data(raw_data, doc, custom_response)
    custom_response.insert_data(data)
    return custom_response

def post_component(
        custom_response,
        component
    ):
    
    # Connect to the database
    try:
        session = get_session()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response
    
    print(component)
        
    try:
        
        # Save Files if Any
        new_component = save_files(component)
        
        # Insert Component in Components Table
        stream = session.execute(
            insert(db.Components).returning(db.Components),
            new_component
        )
        raw_data = stream.all()
        new_component_id = raw_data[0][0].get_id()
        
        # Insert new component_id in Items Table
        stream = session.execute(
            insert(db.Item_id).returning(db.Item_id),
            {"component_id": new_component_id}
        )
        raw_data = stream.all()
        new_item_id = raw_data[0][0].get_id()
        
        
        session.commit()
    except Exception as e:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(400)
        session.rollback()
        return custom_response
    
    session.close()
    
    # Process and Package the data
    custom_response.insert_data(new_component)
    custom_response.set_status_code(201)
    flash_message = FlashMessage(
        message_type=MessageType.SUCCESS, 
        message="Component Added Successfully"
    )
    custom_response.insert_flash_message(flash_message)
    return custom_response

def put_component(
        custom_response,
        component
    ):
    
    component_no_files = remove_file_obj(component)
    
    # Process and Package the data
    custom_response.insert_data(component_no_files)
    custom_response.set_status_code(201)
    flash_message = FlashMessage(
        message_type=MessageType.SUCCESS, 
        message="Component Added Successfully"
    )
    custom_response.insert_flash_message(flash_message)
    return custom_response

def remove_file_obj(data):
    if 'doc' in data.keys():
        flag = False
        if "files" in data["doc"].keys() and len(data["doc"]["files"]) > 0:
            for file in data["doc"]["files"].keys():
                keys = data["doc"]["files"][file].keys()
                if 'file_obj' in keys:
                    flag = True
                    data["doc"]["files"][file].pop("file_obj")
        if not flag:
            data["doc"].pop("files")
    return data, flag

def save_files(data):
    if 'doc' in data.keys():
        if "files" in data["doc"].keys():
            if len(data["doc"]["files"]) > 0:
                pop_list = []
                save = {}
                for file in data["doc"]["files"].keys():
                    compare = ["file_obj", "filename", "type"]
                    keys = data["doc"]["files"][file].keys()
                    values = list(data["doc"]["files"][file].values())
                    if len(compare & keys) == 3 and all(values):
                        file_data = data["doc"]["files"][file]
                        file_hash = save_file(file_data)
                        data["doc"]["files"][file].pop("file_obj")
                        save[file_hash] = data["doc"]["files"][file].copy()
                    else:
                        raise Exception("Missing File Information.")
                    pop_list.append(file)
            if len(pop_list) > 0:
                for file in pop_list:
                    data["doc"]["files"].pop(file)
                data["doc"]["files"] = save
        else:
            raise Exception("No files to save")
    return data


def save_file(file_data):
    file_hash = md5_from_file(file_data["file_obj"])
    print(file_hash)
    print(file_data["filename"])
    print(file_data["type"])
    return file_hash

import hashlib

def md5_from_file(file, block_size=2**14):
    md5 = hashlib.md5()
    while True:
        data = file.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()