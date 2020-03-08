from jovian.utils.misc import urljoin
from jovian.utils.credentials import read_api_url


def _u(path):
    """Make a URL from the path"""
    return urljoin(read_api_url(), path)


def _v(version):
    """Create version query parameter string"""
    if version is not None:
        return "?gist_version=" + str(version)
    return ""
