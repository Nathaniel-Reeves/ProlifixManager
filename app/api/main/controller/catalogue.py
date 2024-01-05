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
        
    try:
        
        # Save Files if Any
        new_component = save_files(component, session)
        
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
        
        # Insert Component_Names in Component_Names Table
        for name in new_component["Component_Names"]:
            name["component_id"] = new_component_id
            stream = session.execute(
                insert(db.Component_Names).returning(db.Component_Names),
                name
            )
            raw_data = stream.all()
            name["name_id"] = raw_data[0][0].get_id()
        
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

def save_files(data, session):
    if 'doc' in data.keys():
        if "files" in data["doc"].keys():
            if len(data["doc"]["files"]) > 0:
                pop_list = []
                save = {}
                for file in data["doc"]["files"].keys():
                    compare = ["file_obj", "filename", "type", "page", "id_code"]
                    keys = data["doc"]["files"][file].keys()
                    values = list(data["doc"]["files"][file].values())
                    if len(compare & keys) == 5 and all(values):
                        file_data = data["doc"]["files"][file]
                        file_hash, filename = save_file(file_data, session)
                        data["doc"]["files"][file].pop("file_obj")
                        save[file_hash] = data["doc"]["files"][file].copy()
                        save[file_hash]["filename"] = filename
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


from flask import (
    current_app as app
)
import os
import pathlib
from werkzeug.utils import secure_filename

def save_file(file_data, session):
    
    # Get File Hash
    file_hash = md5_from_file(file_data["file_obj"])
    
    # Check if File Exists in DB, Save if not
    stream = session.execute(
        select(db.Files).where(db.Files.file_hash == file_hash)
    )
    raw_data = stream.all()
    
    if len(raw_data) > 0:
        return raw_data[0][0].get_id(), raw_data[0][0].file_name
        
    # Save File to Filesystem
    
    # Create File Name
    fn = secure_filename(
        str(file_data["filename"]).replace(" ", "_").replace("/","-")
    )
    id_code = secure_filename(
        str(file_data["id_code"]).replace(" ", "_").replace("/","-")
    )
    page = secure_filename(
        str(file_data["page"]).replace(" ", "_").replace("/","-")
    )

    filename = f"{file_hash}║fn[{fn}]║id_code[{id_code}]║pg[{page}]║"
    
    if file_data["file_obj"].content_type == "application/pdf":
        filename += ".pdf"
    
    # Create Directory if it doesn't already exist
    directory = os.path.join(
        app.config['UPLOAD_FOLDER'], file_data["type"]
    )

    pathlib.Path(
        directory
    ).mkdir(exist_ok=True, parents=True)
    
    path = os.path.join(
        directory, filename
    )

    # Save File
    print(file_data["file_obj"].stream.read())
    file_data["file_obj"].save(path)
    file_data["file_obj"].close()
    
    # Save File Info in DB
    stream = session.execute(
        insert(db.Files).returning(db.Files),
        {
            "file_hash": file_hash,
            "file_name": fn,
            "file_type": file_data["type"],
            "id_code": file_data["id_code"],
            "pg": file_data["page"],
        }
    )
    raw_data = stream.all()
    new_file_id = raw_data[0][0].get_id()
    if new_file_id != file_hash:
        session.rollback()
        raise Exception("File Hash Mismatch")
    else:
        # session.commit()
        session.rollback()

    return file_hash, filename

import hashlib

def md5_from_file(file, block_size=2**14):
    md5 = hashlib.md5()
    while True:
        data = file.read(block_size)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()