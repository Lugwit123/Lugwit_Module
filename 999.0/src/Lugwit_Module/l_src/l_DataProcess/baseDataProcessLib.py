def get_dict_nested_value(dictionary, keys):
    if not isinstance(dictionary, dict) or len(keys) == 0:
        return None
    key = keys[0]
    if key not in dictionary:
        return None
    if len(keys) == 1:
        return dictionary[key]
    return get_dict_nested_value(dictionary[key], keys[1:])