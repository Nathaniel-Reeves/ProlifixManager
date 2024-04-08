"""
Package Data Gathered from Controlers through the Models.
"""
from view.response import (
    error_message
)

def package_data(raw_data, doc, custom_response):
    """
    Package data into json like format, populate child tabels
    as object elements within a list.

    Args:
        raw_data (list): List of tuples containing table objects
        doc (bool): a boolean indicating whether or not to include the document column in the response
        custom_response (CustomResponse): Collects any error or other messages.

    Returns:
        data (dict): Dictionary containing the data in a json like format.
        custom_response (CustomResponse): Collects any error or other messages.
    """
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
                    if table is None:
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