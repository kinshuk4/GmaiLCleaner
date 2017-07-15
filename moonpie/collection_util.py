
def get_multi_level_val_from_dict(dct, path_str, default=None):
    """
    >>> rget({'a': 1}, ['a'])
    1
    >>> rget({'a': {'b': 2}}, ['a', 'b'])
    2
    """
    keys = path_str.split('/')
    return rget(dct, keys, None)


# https://stackoverflow.com/a/27005597/3222727
def rget(dct, keys, default=None):
    """
    >>> rget({'a': 1}, ['a'])
    1
    >>> rget({'a': {'b': 2}}, ['a', 'b'])
    2
    """
    key = keys.pop(0)
    try:
        elem = dct[key]
    except KeyError as e:
        return default
    except TypeError as e:
        # you gotta handle non dict types here
        # beware of sequences when your keys are integers
        print(e)
    if not keys:
        return elem
    return rget(elem, keys, default)