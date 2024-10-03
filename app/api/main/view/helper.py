def only_integers(iterable):
    '''
    Converts python list to python list
    of integer values.
    '''
    for item in iterable:
        try:
            yield int(item)
        except ValueError:
            pass

def str_to_int(string):
    '''
    Converts a string to an integer.
    '''
    if not isinstance(string, str):
        return None
    try:
        return int(string)
    except ValueError:
        return None

def validate_float_in_dict(dictionary, field, minimum=0, maximum=999999, equal_to=True):
    '''
    Validates that the value of a field in a dictionary
    is a float.
    '''
    if field not in dictionary:
        return False
    try:
        float(dictionary[field])
    except ValueError:
        return False
    if equal_to:
        if float(dictionary[field]) <= minimum:
            return False
        if float(dictionary[field]) >= maximum:
            return False
        return True
    if float(dictionary[field]) < minimum:
        return False
    if float(dictionary[field]) > maximum:
        return False
    return True

def validate_int_in_dict(dict, field, min_v=0, max_v=99999999999, equal_to=True):
    '''
    Validates that the value of a field in a dictionary
    is a int.
    '''
    if field not in dict:
        return False
    if isinstance(dict[field], int):
        if equal_to:
            if int(dict[field]) >= min_v and \
            int(dict[field]) < max_v:
                return True
            return False
        if int(dict[field]) > min_v and \
            int(dict[field]) < max_v:
            return True
        return False
    return False

def check_type(valid_types, types_request, empty_means_all=True):
    """
    Checks if the types_request is a list of valid types.

    Args:
        valid_types (list): List if valid strings.
        types_request (list):Requested query in list of strings.
        empty_means_all (bool, optional): if all items in the valid list are selected, return an empty list if True, and the full list if False. Defaults to True.

    Returns:
        List
    """
    types = []
    for type in valid_types:
        if type in types_request:
            types.append(type)
    if empty_means_all and types == valid_types:  # Empty list means get all types
        types = []
    return types
