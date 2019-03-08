"""Utilies the manage the .jovianrc file"""
import os
import json
from jovian.utils.constants import RC_FILENAME


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


def get_notebook_slug(filename):
    """Get the gist slug for a notebook filename"""
    data = get_rcdata()
    if (filename in data['notebooks']):
        return data['notebooks'][filename]['slug']


def set_notebook_slug(filename, slug):
    """Set the gist slug for a notebook filename"""
    data = get_rcdata()
    data['notebooks'][filename] = {'slug': slug}
    save_rcdata(data)


def make_rcdata(filename, slug):
    """Make an JSON string for an individual file"""
    data = {
        "notebooks": {
            filename: {
                "slug": slug
            }
        }
    }
    return json.dumps(data)
