from ...handlers.helper import (
    validate_int_in_dict,
    validate_float_in_dict
)


# Test Cases for validate_float_in_dict()

def test_validate_float_in_dict_valid_float():
    dict = {"foo": 20.5}
    output = validate_float_in_dict(dict, "foo")
    assert output is True

def test_validate_float_in_dict_invalid_type():
    dict = {"foo": "string"}
    output = validate_float_in_dict(dict, "foo")
    assert output is False

def test_validate_float_in_dict_invalid_field():
    dict = {"foo": 20.5}
    output = validate_float_in_dict(dict, "not_foo")
    assert output is False

def test_validate_float_in_dict_empty_dict():
    dict = {}
    output = validate_float_in_dict(dict, "foo")
    assert output is False

def test_validate_float_in_dict_float_under_min():
    dict = {"foo": -20.5}
    output = validate_float_in_dict(dict, "foo")
    assert output is False

def test_validate_float_in_dict_float_over_max():
    dict = {"foo": 1000000.4}
    output = validate_float_in_dict(dict, "foo")
    assert output is False

def test_validate_float_in_dict_float_min():
    dict = {"foo": -0.1}
    output = validate_float_in_dict(dict, "foo")
    assert output is False

def test_validate_float_in_dict_float_min_not_equal_to():
    dict = {"foo": 0.0}
    output = validate_float_in_dict(dict, "foo", equal_to=False)
    assert output is False

def test_validate_float_in_dict_float_max_not_equal_to():
    dict = {"foo": 1000000}
    output = validate_float_in_dict(dict, "foo", equal_to=False)
    assert output is False

def test_validate_float_in_dict_float_change_min():
    dict_1 = {"foo": 1.3}
    output_1 = validate_float_in_dict(dict_1, "foo", min=5.2)
    assert output_1 is False

    dict_2 = {"foo": 7.5}
    output_2 = validate_float_in_dict(dict_2, "foo", min=5.2)
    assert output_2 is True

    dict_3 = {"foo": 5.2}
    output_3 = validate_float_in_dict(dict_3, "foo", min=5.2)
    assert output_3 is True

def test_validate_float_in_dict_float_change_max():
    dict_1 = {"foo": 2}
    output_1 = validate_float_in_dict(dict_1, "foo", max=5.2)
    assert output_1 is False

    dict_2 = {"foo": 5.2}
    output_2 = validate_float_in_dict(dict_2, "foo", max=5.2)
    assert output_2 is True

    dict_3 = {"foo": 7.2}
    output_3 = validate_float_in_dict(dict_3, "foo", max=5.2)
    assert output_3 is True

# Test Cases for validate_int_in_dict()

def test_validate_int_in_dict_valid_int():
    dict = {"foo": 10}
    output = validate_int_in_dict(dict, "foo")
    assert output is True

def test_validate_int_in_dict_invalid_type():
    dict = {"foo": "string"}
    output = validate_int_in_dict(dict, "foo")
    assert output is False

def test_validate_int_in_dict_invalid_field():
    dict = {"foo": 10}
    output = validate_int_in_dict(dict, "not_foo")
    assert output is False

def test_validate_int_in_dict_empty_dict():
    dict = {}
    output = validate_int_in_dict(dict, "foo")
    assert output is False

def test_validate_int_in_dict_int_under_min():
    dict = {"foo": -10}
    output = validate_int_in_dict(dict, "foo")
    assert output is False

def test_validate_int_in_dict_int_over_max():
    dict = {"foo": 100000000000}
    output = validate_int_in_dict(dict, "foo")
    assert output is False

def test_validate_int_in_dict_int_min():
    dict = {"foo": 0}
    output = validate_int_in_dict(dict, "foo")
    assert output is True

def test_validate_int_in_dict_int_min_not_equal_to():
    dict = {"foo": 0}
    output = validate_int_in_dict(dict, "foo", equal_to=False)
    assert output is False

def test_validate_int_in_dict_int_max_not_equal_to():
    dict = {"foo": 100000000000}
    output = validate_int_in_dict(dict, "foo", equal_to=False)
    assert output is False

def test_validate_int_in_dict_int_change_min():
    dict_1 = {"foo": 1}
    output_1 = validate_int_in_dict(dict_1, "foo", min_v=5)
    assert output_1 is False

    dict_2 = {"foo": 6}
    output_2 = validate_int_in_dict(dict_2, "foo", min_v=5)
    assert output_2 is True

    dict_3 = {"foo": 5}
    output_3 = validate_int_in_dict(dict_3, "foo", min_v=5)
    assert output_3 is True

def test_validate_int_in_dict_int_change_max():
    dict_1 = {"foo": 2}
    output_1 = validate_int_in_dict(dict_1, "foo", max_v=5)
    assert output_1 is True

    dict_2 = {"foo": 6}
    output_2 = validate_int_in_dict(dict_2, "foo", max_v=5)
    assert output_2 is False

    dict_3 = {"foo": 5}
    output_3 = validate_int_in_dict(dict_3, "foo", max_v=5)
    assert output_3 is True
