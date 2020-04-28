from jovian.utils.rcfile import get_notebook_slug

_current_slug = None


def set_current_slug(filename):
    global _current_slug
    if _current_slug is None:
        _current_slug = get_notebook_slug(filename)


def get_current_slug():
    global _current_slug
    return _current_slug
