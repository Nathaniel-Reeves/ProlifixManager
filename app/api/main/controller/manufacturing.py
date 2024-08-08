'''
Handle Manufacturing Data
'''
from sqlalchemy import select

from view.response import CustomResponse
import model as db
from .execute import execute_query

def get_processes(
        custom_response,
        process_id,
        populate,
        doc
    ):

    # Build the query
    stm = select(db.Processes)

    if process_id:
        stm = stm.where(db.Processes.process_id.in_(process_id))

    # Execute the query
    custom_response, raw_data, success = execute_query(custom_response, stm)
    if not success:
        return custom_response

    # Process and Package the data
    for row in raw_data:
        pk = row[0].get_id()
        process = row[0].to_dict()
        equipment = {'equipment':[]}

        if 'equipment' in populate:
            r = CustomResponse()
            resp = get_equipment( r, [pk], [], False)
            equipment = {'equipment': resp.get_data()}
            custom_response.insert_flash_messages(r.get_flash_messages())

        custom_response.insert_data({**process, **equipment})

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