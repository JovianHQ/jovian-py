VALID_EXT = ["py"]


def get_file_name():
    try:
        from __main__ import __file__
        return __file__
    except Exception as e:
        return None


def in_script():
    filename = get_file_name()
    if filename is not None:
        ext = filename.split(".")[-1]
        return ext in VALID_EXT

    return False
