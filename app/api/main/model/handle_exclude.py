import logging

def handle_exclude(out, exclude=[]):
    """Overwrites specified keys with None from the output dictionary

    Args:
        out (dict): dictionary to be modified
        exclude (list): list of column names (str) to exclude

    Returns:
        dict: modified dictionary, returns unmodified dictionary if exclude is empty
    """
    if not exclude:
        return out

    if not isinstance(out, dict) or not out:
        logging.error("handle_exclude: Out is empty or wrong type")
        raise ValueError("handle_exclude: Out is empty or wrong type")

    for key in exclude:
        if key == 'timestamp_entered':
            logging.warning("timestamp_entered is not allowed in exclude list")
            continue
        if key == 'timestamp_modified':
            logging.warning("timestamp_modified is not allowed in exclude list")
            continue
        if key == 'timestamp_fetched':
            logging.warning("timestamp_fetched is not allowed in exclude list")
            continue
        out[key] = None
        logging.debug(f"handle_exclude: Excluded key {key}")

    return out