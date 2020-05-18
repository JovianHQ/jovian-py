from jovian.utils.rcfile import get_notebook_slug

_current_slug = None


def set_current_slug(filename):
    """ Helper function to set current slug from notebook extension"""
    global _current_slug
    _current_slug = get_notebook_slug(filename)


def get_current_slug():
    global _current_slug
    return _current_slug
