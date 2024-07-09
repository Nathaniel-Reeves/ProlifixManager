'''
Handle Inventory Data
'''
from sqlalchemy import select

from view.response import CustomResponse
import model as db
from .execute import execute_query

import controller.organizations as org
from .orders import get_purchase_order_detail

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
    stm = select(db.Components, db.Item_id, db.Component_Names)
    stm = stm.join(db.Item_id, db.Components.component_id == db.Item_id.component_id, isouter=True)
    stm = stm.join(db.Component_Names, db.Components.primary_name_id == db.Component_Names.name_id, isouter=True)

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
        if 'wildcrafted' in certifications:
            stm = stm.where(db.Components.certified_wildcrafted == True)
        if 'made_with_organic' in certifications:
            stm = stm.where(db.Components.certified_made_with_organic == True)
        if 'gmp' in certifications:
            stm = stm.where(db.Components.certified_gmp == True)
        if 'fda' in certifications:
            stm = stm.where(db.Components.certified_fda == True)

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        component = row[0].to_dict()

        if row[1]:
            item_id = row[1].get_id()
            component['item_id'] = item_id
        else:
            component['item_id'] = None

        if row[2]:
            component_primary_name = row[2].to_dict()
            component['component_primary_name'] = component_primary_name['component_name']
        else:
            component['component_primary_name'] = None

        component_names = {'component_names':[]}
        purchase_order_detail = {'purchase_order_detail':[]}
        inventory = {'inventory':[]}
        brand = {'brand':[]}

        if 'component_names' in populate:
            r = CustomResponse()
            resp = get_component_names( r, [], [pk], False, False)
            component_names = {'component_names':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'purchase_order_detail' in populate:
            r = CustomResponse()
            resp = get_purchase_order_detail( r, [], [], False)
            purchase_order_detail = {'purchase_order_detail':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'inventory' in populate:
            r = CustomResponse()
            resp = get_inventory( r, [], [item_id], [], [], False)
            inventory = {'inventory':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'brand' in populate:
            r = CustomResponse()
            resp = org.get_organizations( r, [component.brand_id], [], [], False)
            brand = {'brand':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if not doc:
            component.pop('doc')

        custom_response.insert_data({**component, **component_names, **purchase_order_detail, **inventory, **brand})

    return custom_response

def get_component_names(
        custom_response,
        name_ids,
        component_ids,
        primary_name=False,
        botanical_name=False
    ):

    # Build the query
    stm = select(db.Component_Names)

    if name_ids:
        stm = stm.where(db.Component_Names.name_id.in_(name_ids))

    if component_ids:
        stm = stm.where(db.Component_Names.component_id.in_(component_ids))

    if primary_name:
        stm = stm.where(db.Component_Names.primary_name == True)

    if botanical_name:
        stm = stm.where(db.Component_Names.botanical_name == True)

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        component_name = row[0].to_dict()

        custom_response.insert_data({ **component_name })

    return custom_response

def get_inventory(
        custom_response,
        inv_ids,
        item_ids,
        lot_numbers,
        owners,
        doc
    ):
    raise NotImplementedError