VALID_EXT = ["py"]


def get_script_filename():
    try:
        from __main__ import __file__
        return __file__
    except:
        return None


def in_script():
    filename = get_script_filename()
    if filename is not None:
        ext = filename.split(".")[-1]
        return ext in VALID_EXT

    return False
