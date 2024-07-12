'''
Handle Product Data
'''
from sqlalchemy import select

from view.response import CustomResponse
import model as db
from .execute import execute_query

def get_products(
        custom_response,
        product_ids,
        certifications,
        client_ids,
        populate,
        doc
    ):

    # Build the query
    tables = [db.Product_Master, db.Organization_Names]
    stm = select(*tables)
    stm = stm.join(db.Organization_Names, db.Product_Master.organization_id == db.Organization_Names.organization_id, isouter=True)
    stm = stm.where(db.Organization_Names.primary_name == True)

    if product_ids:
        stm = stm.where(db.Product_Master.product_id.in_(product_ids))

    if client_ids:
        stm = stm.where(db.Product_Master.organization_id.in_(client_ids))

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

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        product_master = row[0].to_dict()
        organization_names = row[1].to_dict()
        formulas = {'formulas':[]}
        manufacturing = {'manufacturing': []}

        # Populate
        if ('manufacturing' in populate) or ('components' in populate):
            r = CustomResponse()
            resp = get_manufacturing( r, [pk], ['components', 'equipment'], doc)
            manufacturing_nodes = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())

            r = CustomResponse()
            resp = get_manufacturing_edges( r, [pk])
            manufacturing_edges = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())

            manufacturing = {'manufacturing':{'nodes': manufacturing_nodes, 'edges': manufacturing_edges}}

        if 'formulas' in populate:
            r = CustomResponse()
            resp = get_formulas( r, [], [pk], ['formula_detail'], doc)
            formulas = {'formulas': resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({**product_master, **organization_names, **formulas, **manufacturing})

    return custom_response

def get_manufacturing(
        custom_response,
        product_ids,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.Manufacturing_Process, db.Processes)
    stm = stm.join(db.Processes, db.Manufacturing_Process.manufacturing_process_id == db.Processes.process_id, isouter=True)

    if product_ids:
        stm = stm.where(db.Manufacturing_Process.product_id.in_(product_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        process_pk = row[1].get_id()
        manufacturing_nodes = {**row[0].to_dict(), **row[1].to_dict()}
        equipment = {'equipment':[]}
        components = {'components':[]}

        if 'components' in populate:
            r = CustomResponse()
            resp = get_process_components( r, [pk], [], False)
            components = {'components':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'equipment' in populate:
            r = CustomResponse()
            resp = get_equipment( r, [process_pk], [], False)
            equipment = {'equipment':resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({**manufacturing_nodes, **components, **equipment})

    return custom_response

def get_manufacturing_edges(
        custom_response,
        product_ids
    ):

    # Build the query
    stm = select(db.Manufacturing_Process_Edges)

    if product_ids:
        stm = stm.where(db.Manufacturing_Process_Edges.product_id.in_(product_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        manufacturing_edges = row[0].to_dict()

        custom_response.insert_data({**manufacturing_edges})

    return custom_response

def get_equipment(
        custom_response,
        process_id,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.Equipment)

    if process_id:
        stm = stm.where(db.Equipment.process_id.in_(process_id))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        equipment = row[0].to_dict()

        custom_response.insert_data({**equipment})

    return custom_response

def get_process_components(
        custom_response,
        process_spec_ids,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.Process_Components)

    if process_spec_ids:
        stm = stm.where(db.Process_Components.process_spec_id.in_(process_spec_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        process_components = row[0].to_dict()

        # Populate
        r = CustomResponse()
        resp = get_components( r, [pk], [], False)
        components = {'components':resp.get_data()}
        custom_response.insert_flash_messages(r.get_flash_messages())

        r = CustomResponse()
        resp = get_component_brands( r, [pk], [], False)
        brand_info = {'brands':resp.get_data()}
        custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({**process_components, **components, **brand_info})

    return custom_response

def get_component_brands(
        custom_response,
        process_component_ids,
        brand_ids,
        doc
    ):

    # Build the query
    stm = select(db.Component_Brands_Join, db.Organization_Names)

    stm = stm.join(db.Organization_Names, db.Component_Brands_Join.brand_id == db.Organization_Names.organization_id, isouter=True)
    stm = stm.where(db.Organization_Names.primary_name == True)

    if process_component_ids:
        stm = stm.where(db.Component_Brands_Join.process_component_id.in_(process_component_ids))

    if brand_ids:
        stm = stm.where(db.Organization_Names.organization_id.in_(brand_ids))

    stm = stm.order_by(db.Component_Brands_Join.priority)

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        component_brand = row[1].to_dict()
        component_brand_join = row[0].to_dict()
        component_brand['organization_primary_name'] = component_brand['organization_name']
        component_brand['organization_primary_initial'] = component_brand['organization_initial']

        custom_response.insert_data({**component_brand_join, **component_brand})

    return custom_response

def get_components(
        custom_response,
        process_component_ids,
        component_ids,
        doc
    ):

    # Build the query
    stm = select(db.Components_Join, db.Component_Names, db.Components)

    stm = stm.join(db.Components, db.Components_Join.component_id == db.Components.component_id, isouter=True)
    stm = stm.join(db.Component_Names, db.Components_Join.component_id == db.Component_Names.component_id, isouter=True)
    stm = stm.where(db.Component_Names.primary_name == True)

    if process_component_ids:
        stm = stm.where(db.Components_Join.process_component_id.in_(process_component_ids))

    if component_ids:
        stm = stm.where(db.Components_Join.component_id.in_(component_ids))

    stm = stm.order_by(db.Components_Join.priority)

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        component_join = row[0].to_dict()
        component_name = row[1].to_dict()
        component_info = row[2].to_dict()

        if not doc:
            component_info.pop('doc')

        custom_response.insert_data({**component_join, **component_name, **component_info})

    return custom_response

def get_formulas(
        custom_response,
        formula_ids,
        product_ids,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.Formula_Master)

    if formula_ids:
        stm = stm.where(db.Formula_Master.formula_id.in_(formula_ids))

    if product_ids:
        stm = stm.where(db.Formula_Master.product_id.in_(product_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        formulas_master = row[0].to_dict()
        formula_detail = {'formula_detail':[]}

        # Populate
        if 'formula_detail' in populate:
            r = CustomResponse()
            resp = get_formula_detail( r, [pk], [], False)
            formula_detail = {'formula_detail': resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({**formulas_master, **formula_detail})

    return custom_response

def get_formula_detail(
        custom_response,
        formula_ids,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.Formula_Detail)

    if formula_ids:
        stm = stm.where(db.Formula_Detail.formula_id.in_(formula_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        formula_detail = row[0].to_dict()

        # Populate
        r = CustomResponse()
        resp = get_ingredients( r, [pk], [], False)
        ingredient_info = {'ingredients_detail': resp.get_data()}
        custom_response.insert_flash_messages(r.get_flash_messages())

        r = CustomResponse()
        resp = get_ingredient_brands( r, [pk], [], False)
        brand_info = {'brands': resp.get_data()}
        custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({**formula_detail, **ingredient_info, **brand_info})

    return custom_response

def get_ingredient_brands(
        custom_response,
        formula_ingredient_ids,
        brand_ids,
        doc
    ):

    # Build the query
    stm = select(db.Ingredient_Brands_Join, db.Organization_Names)

    stm = stm.join(db.Organization_Names, db.Ingredient_Brands_Join.brand_id == db.Organization_Names.organization_id, isouter=True)
    stm = stm.where(db.Organization_Names.primary_name == True)

    if formula_ingredient_ids:
        stm = stm.where(db.Ingredient_Brands_Join.formula_ingredient_id.in_(formula_ingredient_ids))

    if brand_ids:
        stm = stm.where(db.Organization_Names.organization_id.in_(brand_ids))

    stm = stm.order_by(db.Ingredient_Brands_Join.priority)

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        ingredient_brand_join = row[0].to_dict()
        ingredient_brand = row[1].to_dict()
        ingredient_brand['organization_primary_name'] = ingredient_brand['organization_name']
        ingredient_brand['organization_primary_initial'] = ingredient_brand['organization_initial']

        custom_response.insert_data({**ingredient_brand, **ingredient_brand_join})

    return custom_response

def get_ingredients(
        custom_response,
        formula_ingredient_ids,
        ingredient_ids,
        doc
    ):

    # Build the query
    stm = select(db.Ingredients_Join, db.Component_Names, db.Components)

    stm = stm.join(db.Components, db.Ingredients_Join.ingredient_id == db.Components.component_id, isouter=True)
    stm = stm.join(db.Component_Names, db.Ingredients_Join.ingredient_id == db.Component_Names.component_id, isouter=True)
    stm = stm.where(db.Component_Names.primary_name == True)

    if formula_ingredient_ids:
        stm = stm.where(db.Ingredients_Join.formula_ingredient_id.in_(formula_ingredient_ids))

    if ingredient_ids:
        stm = stm.where(db.Ingredients_Join.ingredient_id.in_(ingredient_ids))

    stm = stm.order_by(db.Ingredients_Join.priority)

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        ingredient_join = row[0].to_dict()
        ingredient_name = row[1].to_dict()
        ingredient_info = row[2].to_dict()

        if not doc:
            ingredient_info.pop('doc')

        custom_response.insert_data({ **ingredient_join, **ingredient_name, **ingredient_info})

    return custom_response
