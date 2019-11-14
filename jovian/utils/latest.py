import requests
from random import random

from jovian._version import __version__
from jovian.utils.logger import log
from pkg_resources import parse_version


def get_latest_version():
    """Returns Jovian's latest pypi version.

    When Internet connection is not available it assumes 
    the current version as the latest version.
    """

    pypi_json = 'https://pypi.org/pypi/jovian/json'
    try:
        latest_version = requests.get(pypi_json, timeout=3).json()['info']['version']
    except:
        latest_version = __version__

    return latest_version


def check_update(probability=.2):
    """Check if there is a update available and logs
    current and latest version with the command to update
    the library.

    Args:
        probability (float, optional): Approximate probability with which the user
                                    is notified. Defaults to .2(~20%).
                                    (1 == always)
    """
    if random() < probability:
        latest_version = parse_version(get_latest_version())
        current_version = parse_version(__version__)
        if latest_version > current_version:
            log('Update Available: {0} --> {1}'.format(__version__, latest_version))
            log('Run `!pip install jovian --upgrade` to upgrade')
