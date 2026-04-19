def get_element_with_default(lst, index, default=None):
    return lst[index] if index < len(lst) else default
