'''
Handle Product Data
'''
import json
from sqlalchemy import select, insert, update, delete

from view.response import (
    VariantType,
    FlashMessage,
    error_message
)
import model as db
from model.connector import get_session
from .package import package_data
from .files import save_files

def get_products(
        custom_response,
        product_ids,
        product_types,
        certifications,
        client_ids,
        populate,
        doc
    ):

    # Build the query
    tables = [db.Product_Master, db.Organization_Names]

    if 'inventory' in populate:
        tables.append(db.Inventory)
    if 'lot-numbers' in populate:
        tables.append(db.Lot_Numbers)
    if 'default-formula' in populate:
        tables.append(db.Formula_Master)
        tables.append(db.Formula_Detail)
    if 'manufacturing-process' in populate or 'components' in populate:
        tables.append(db.Manufacturing_Process)

    stm = select(*tables)
    stm = stm.join(db.Organization_Names, db.Product_Master.organization_id == db.Organization_Names.organization_id, isouter=True)

    if 'inventory' in populate:
        stm = stm.join(db.Item_id, db.Product_Master.product_id == db.Item_id.product_id, isouter=True)
        stm = stm.join(db.Inventory, db.Item_id.item_id == db.Inventory.item_id, isouter=True)
    if 'lot-numbers' in populate:
        stm = stm.join(db.Lot_Numbers, db.Product_Master.product_id == db.Lot_Numbers.product_id, isouter=True)
    if 'default-formula' in populate:
        stm = stm.join(db.Formula_Master, db.Product_Master.default_formula_id == db.Formula_Master.formula_id, isouter=True)
        stm = stm.join(db.Formula_Detail, db.Formula_Master.formula_id == db.Formula_Detail.formula_id, isouter=True)
    if 'manufacturing-process' in populate or 'components' in populate:
        stm = stm.join(db.Manufacturing_Process, db.Product_Master.product_id == db.Manufacturing_Process.product_id, isouter=True)

    stm = stm.where(db.Organization_Names.primary_name == True)

    if product_ids:
        stm = stm.where(db.Product_Master.product_id.in_(product_ids))

    if client_ids:
        stm = stm.where(db.Product_Master.organization_id.in_(client_ids))

    if product_types:
        stm = stm.where(db.Product_Master.type.in_(product_types))

    if 'lot-numbers' in populate:
        stm = stm.order_by(db.Lot_Numbers.year)
        stm = stm.order_by(db.Lot_Numbers.month)
        stm = stm.order_by(db.Lot_Numbers.sec_number)

    if certifications:
        if 'usda_organic' in certifications:
            stm = stm.where(db.Product_Master.certified_usda_organic == True)
        if 'halal' in certifications:
            stm = stm.where(db.Product_Master.certified_halal == True)
        if 'kosher' in certifications:
            stm = stm.where(db.Product_Master.certified_kosher == True)
        if 'gluten_free' in certifications:
            stm = stm.where(db.Product_Master.certified_gluten_free == True)
        if 'national-sanitation-foundation' in certifications:
            stm = stm.where(db.Product_Master.certified_national_sanitation_foundation == True)
        if 'us-pharmocopeia' in certifications:
            stm = stm.where(db.Product_Master.certified_us_pharmacopeia == True)
        if 'non_gmo' in certifications:
            stm = stm.where(db.Product_Master.certified_non_gmo == True)
        if 'vegan' in certifications:
            stm = stm.where(db.Product_Master.certified_vegan == True)
        if 'wildcrafted' in certifications:
            stm = stm.where(db.Product_Master.certified_wildcrafted == True)
        if 'made_with_organic' in certifications:
            stm = stm.where(db.Product_Master.certified_made_with_organic == True)
        if 'gmp' in certifications:
            stm = stm.where(db.Product_Master.certified_gmp == True)
        if 'fda' in certifications:
            stm = stm.where(db.Product_Master.certified_fda == True)

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
        session.close()
        return custom_response

    session.close()
    # Process and Package the data
    print(raw_data)
    data, custom_response = package_data(raw_data, doc, custom_response)
    custom_response.insert_data(data)
    return custom_response