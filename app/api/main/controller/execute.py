from view.response import error_message
from model.connector import get_session

def execute_query(custom_response, stm):
    raw_data = []

    # Connect to the database
    try:
        session = get_session()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(500)
        return custom_response, raw_data, False

    # Execute the query
    try:
        stream = session.execute(stm)
        raw_data = stream.all()
    except Exception:
        error = error_message()
        custom_response.insert_flash_message(error)
        custom_response.set_status_code(400)
        session.close()
        return custom_response, raw_data, False

    session.close()
    return custom_response, raw_data, True