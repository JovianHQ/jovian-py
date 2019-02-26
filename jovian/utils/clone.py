import os
from requests import get
from jovian.utils.constants import API_URL
from jovian._version import __version__
from jovian.utils.logger import log


def _u(path):
    """Make a URL from the path"""
    return API_URL + path


def _msg(res):
    try:
        data = res.json()
        if 'errors' in data and len(data['errors'] > 0):
            return data['errors'][0]['message']
        if 'message' in data:
            return data['message']
        if 'msg' in data:
            return data['msg']
    except:
        if res.text:
            return res.text
        return 'Something went wrong'


def _pretty(res):
    """Make a human readable output from an HTML response"""
    return '(HTTP ' + str(res.status_code) + ') ' + _msg(res)


def _h():
    """Create a header to provide library metadata"""
    return {"x-jovian-source": "library",
            "x-jovian-library-version": __version__}


def get_gist(slug):
    """Download a gist"""
    res = get(url=_u('/gist/' + slug), headers=_h())
    if res.status_code == 200:
        return res.json()['data']
    raise Exception('Failed to retrieve Gist: ' + _pretty(res))


def clone(slug):
    """Download the files for a gist"""
    log('Fetching ' + slug + "..")
    gist = get_gist(slug)
    title = gist['title']
    if os.path.exists(title):
        i = 1
        while os.path.exists(title + '-' + str(i)):
            i += 1
        title = title + '-' + str(i)
    if not os.path.exists(title):
        os.makedirs(title)
    log('Downloading files..')
    for f in gist['files']:
        with open(title + '/' + f['filename'], 'wb') as fp:
            fp.write(get(f['rawUrl']).content)
    log('Cloned successfully to ' + title)
