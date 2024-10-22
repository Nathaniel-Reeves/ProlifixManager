'''
Handle Organizations Data
'''
from sqlalchemy import select

from view.response import CustomResponse
import model as db
from .execute import execute_query

from .orders import get_sales_orders, get_purchase_orders
from .inventory import get_component_suppliers, get_components
from .products import get_products


def get_organizations(
        custom_response,
        org_ids,
        org_type,
        populate,
        doc
    ):

    # Build the query
    stm_1 = select(db.Organizations, db.Organization_Names)

    stm_1 = stm_1.join(db.Organization_Names, db.Organizations.primary_name_id == db.Organization_Names.name_id)

    if org_type:
        if 'client' in org_type:
            stm_1 = stm_1.where(db.Organizations.client == True)
        if 'supplier' in org_type:
            stm_1 = stm_1.where(db.Organizations.supplier == True)
        if 'lab' in org_type:
            stm_1 = stm_1.where(db.Organizations.lab == True)
        if 'courier' in org_type:
            stm_1 = stm_1.where(db.Organizations.courier == True)

    if org_ids:
        stm_1 = stm_1.where(db.Organizations.organization_id.in_(org_ids))

    # Execute the query
    custom_response, raw_data_1, success = execute_query(custom_response, stm_1)
    if not success:
        return custom_response

    # Build the query
    if 'organization_names' in populate:
        stm_2 = select(db.Organization_Names).order_by(db.Organization_Names.organization_id)

        # Execute the query
        custom_response, raw_data_2, success = execute_query(custom_response, stm_2)
        if not success:
            return custom_response

    # Process and Package the data
    for row in raw_data_1:
        pk = row[0].get_id()
        organization = row[0].to_dict()

        if row[1]:
            organization_primary_name = row[1].to_dict()
            organization['organization_primary_name'] = organization_primary_name['organization_name']
            organization['organization_primary_initial'] = organization_primary_name['organization_initial']
        else:
            organization['organization_primary_name'] = None
            organization['organization_primary_initial'] = None

        organization_names = {'organization_names': []}
        facilities = {'facilities':[]}
        sales_orders = {'sales_orders': []}
        purchase_orders = {'purchase_orders': []}
        people = {'people': []}
        components = {'components': []}
        products = {'products': []}
        supplies = {'supplies': []}

        # Populate
        if ('organization_names' in populate):
            remove_names = []
            for row in raw_data_2:
                name = row[0].to_dict()
                if name['organization_id'] == pk:
                    organization_names['organization_names'].append(name)
                    remove_names.append(name['name_id'])

            for i, row in enumerate(raw_data_2):
                if row[0].to_dict()['name_id'] in remove_names:
                    raw_data_2.pop(i)
                    remove_names.remove(row[0].to_dict()['name_id'])

        if ('facilities' in populate):
            r = CustomResponse()
            resp = get_facilities( r, [], [pk], [], doc)
            facilities_data = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())
            facilities = {'facilities': facilities_data}

        if ('sales_orders' in populate):
            r = CustomResponse()
            resp = get_sales_orders(r, [], [pk], doc)
            sales_orders_data = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())
            sales_orders = {'sales_orders': sales_orders_data}

        if ('purchase_orders' in populate):
            r = CustomResponse()
            resp = get_purchase_orders(r, [], [pk], doc)
            purchase_orders_data = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())
            purchase_orders = {'purchase_orders': purchase_orders_data}

        if ('people' in populate):
            r = CustomResponse()
            resp = get_people(r, [], [pk], [], doc)
            people_data = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())
            people = {'people': people_data}

        if ('components' in populate):
            r = CustomResponse()
            resp = get_components(r, [], [], [], [pk], [], False)
            components_data = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())
            components = {'components': components_data}

        if 'supplies' in populate:
            r = CustomResponse()
            resp = get_component_suppliers(r, [], [pk])
            if r.get_status_code() != 200:
                custom_response.set_status_code(r.get_status_code())
            else:
                supplies_data = resp.get_data()
                supplies = {'supplies': supplies_data }
            custom_response.insert_flash_messages(r.get_flash_messages())

        if ('products' in populate):
            r = CustomResponse()
            resp = get_products(r, [], [], [pk], [], doc)
            products_data = resp.get_data()
            custom_response.insert_flash_messages(r.get_flash_messages())
            products = {'products': products_data}

        custom_response.insert_data({**organization, **organization_names, **facilities, **sales_orders, **purchase_orders, **people, **components, **products, **supplies})

    return custom_response

def get_organization_names(
        custom_response,
        name_ids,
        organization_ids,
        primary_name=False
    ):

    # Build the query
    stm = select(db.Organization_Names)

    if name_ids:
        stm = stm.where(db.Organization_Names.name_id.in_(name_ids))

    if organization_ids:
        stm = stm.where(db.Organization_Names.organization_id.in_(organization_ids))

    if primary_name:
        stm = stm.where(db.Organization_Names.primary_name == True)

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        organization_name = row[0].to_dict()

        custom_response.insert_data({ **organization_name })

    return custom_response

def get_facilities(
        custom_response,
        facility_ids,
        organization_ids,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.Facilities)

    if facility_ids:
        stm = stm.where(db.Facilities.facility_id.in_(facility_ids))

    if organization_ids:
        stm = stm.where(db.Facilities.organization_id.in_(organization_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        facility = row[0].to_dict()
        org_id = row[0].organization_id

        organizations = {'organizations': []}

        if 'organizations' in populate:
            r = CustomResponse()
            resp = get_organizations(r, [org_id], [], [], doc)
            organizations = {'organizations': resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({ **facility, **organizations })

    return custom_response

def get_people(
        custom_response,
        person_ids,
        organization_ids,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.People)

    if person_ids:
        stm = stm.where(db.People.person_id.in_(person_ids))

    if organization_ids:
        stm = stm.where(db.People.organization_id.in_(organization_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        org_id = row[0].organization_id
        person = row[0].to_dict()

        users = {'user': []}
        organizations = {'organizations': []}

        if 'users' in populate:
            r = CustomResponse()
            resp = get_users(r, [], [pk], doc)
            users = {'users': resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        if 'organizations' in populate:
            r = CustomResponse()
            resp = get_organizations(r, [org_id], [], [], doc)
            organizations = {'organizations': resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({ **person, **users, **organizations })

    return custom_response

def get_users(
        custom_response,
        user_ids,
        person_ids,
        doc
    ):

    # Build the query
    stm = select(db.Users)

    if user_ids:
        stm = stm.where(db.Users.user_id.in_(user_ids))

    if person_ids:
        stm = stm.where(db.Users.person_id.in_(person_ids))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        user = row[0].to_dict()

        custom_response.insert_data({ **user })

    return custom_response

# from sqlalchemy import select, text

# def organization_exists(names, custom_response):
#     """
#     Check if an organization already exists by organization name.
#     """
#     # Execute Querys
#     primary_exists = False
#     levenshtein_results = []
#     for name in names:
#         if name["primary_name"]:
#             primary_exists = True
#         results, levensthein_messages = check_org_exists_levenshtein(
#             name["organization_name"])
#         if not results == -1:
#             levenshtein_results += results
#         custom_response.insert_flash_messages(levensthein_messages)

#     # Handle Primary False
#     if not primary_exists:
#         e_message = FlashMessage(
#             message="Primary Name not selected!",
#             variant=VariantType.WARNING)
#         custom_response.insert_flash_message(e_message)

#     # Insert the levenshtein_results into the response
#     custom_response.insert_data(levenshtein_results)

#     return custom_response


# def check_org_exists_levenshtein(search_name):
#     '''
#     Checks likelyhood if Organization Name already exists
#     in the Database.
#     '''
#     try:
#         session = get_session()

#         # Build Query
#         base_query = """
#         SELECT
#             JSON_OBJECT(
#                 'organization_id', `organization_id`,
#                 'organization_name', `organization_name`,
#                 'levenshtein_probability', CAST(sys.LEVENSHTEIN_RATIO(`organization_name`, :search_name) AS UNSIGNED INTEGER)
#             ) AS levenshtein_results
#         FROM `Organizations`.`Organization_Names`
#         WHERE
#             sys.LEVENSHTEIN_RATIO(`organization_name`, :search_name) > 50;
#         """

#         # Execute Query
#         result = session.execute(
#             text(base_query),
#             {"search_name":search_name}
#         )

#         # Return Results
#         levensthein_results = []
#         levensthein_messages = []
#         for row in result:
#             # Save Data
#             json_row = json.loads(row[0])
#             levensthein_results.append(json_row)

#             # Create Message Components
#             message_alert_heading = "Possible Duplicate Organization."
#             message = f"Possible duplicate organization between '{search_name}' and '{json_row['organization_name']}'."
#             message_detail = f"'{search_name}' is a {json_row['levenshtein_probability']} percent match for '{json_row['organization_name']}'.  Are they the same organization?"
#             message_link = f"/api/organizations/?org-id={json_row['organization_id']}"

#             # Create Message Object using Components
#             message_obj = FlashMessage(
#                 alert_heading=message_alert_heading,
#                 message=message,
#                 message_detail=message_detail,
#                 link=message_link,
#                 variant=VariantType.WARNING
#             )
#             levensthein_messages.append(message_obj)

#         return levensthein_results, levensthein_messages

#     except Exception:
#         error = error_message()
#         return -1, [error]
