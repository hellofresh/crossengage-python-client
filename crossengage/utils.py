def update_dict(old_dict, values):
    """ Update dictionary without change the original object """
    new_dict = old_dict.copy()
    new_dict.update(values)
    return new_dict
