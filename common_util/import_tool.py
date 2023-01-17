# coding: utf-8

def import_by_name(name_str, namespace: dict = None):
    """
    from xxx import xxx
    :param name_str:
    :param namespace:
    :return:
    """
    comp = name_str.split('.')[-1]
    if namespace:
        return namespace[comp]
    mod_path = '.'.join(name_str.split('.')[:-1])
    return getattr(__import__(mod_path, globals(), locals(), [comp]), comp)