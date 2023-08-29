from ...handlers.helper import validate_int_in_dict

# Test validate_int_in_dict

def test_validate_int_in_dict_valid():
    assert validate_int_in_dict({'a': 1, 'b': 2}, 'a') is True
    assert validate_int_in_dict({'a': 1.0, 'b': 2}, 'b') is True