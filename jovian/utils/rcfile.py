"""Utilies to manage the .jovianrc file"""
import os
import json
from jovian.utils.constants import RC_FILENAME

_current_slug = None
_current_project = None


def rcfile_exists():
    """Check if .jovianrc exists"""
    return os.path.exists(RC_FILENAME)


def save_rcdata(data=None):
    """Save given data (or empty) to file"""
    if data is None:
        data = {'notebooks': {}}
    with open(RC_FILENAME, 'w') as f:
        json.dump(data, f, indent=2)


def get_rcdata():
    """Read .jovianrc file as a dict"""
    if not rcfile_exists():
        save_rcdata()
    with open(RC_FILENAME, 'r') as f:
        data = json.load(f)
    return data


def get_notebook_slug(filename, cache_result=True):
    """Get the gist slug for a notebook filename"""
    global _current_slug
    data = get_rcdata()
    if (filename in data.get('notebooks', {})):
        slug = data['notebooks'][filename]['slug']
        if slug and cache_result:
            _current_slug = slug
        return slug


def get_cached_slug():
    """Get the cached notebook slug"""
    global _current_slug
    return _current_slug


def set_notebook_slug(filename, slug, cache_result=True):
    """Set the gist slug for a notebook filename"""
    global _current_slug
    data = get_rcdata()
    data['notebooks'][filename] = {'slug': slug}
    save_rcdata(data)
    if cache_result:
        _current_slug = slug
    return slug


def reset_notebook_slug():
    """Reset cached notebook slug"""
    global _current_slug
    _current_slug = None


def make_rcdata(filename, slug):
    """Make a JSON string for an individual file"""
    data = {
        "notebooks": {
            filename: {
                "slug": slug
            }
        }
    }
    return json.dumps(data)


def get_project():
    """Get cached project parameter"""
    global _current_project
    return _current_project


def set_project(project):
    """Cache project parameter"""
    global _current_project
    _current_project = project
