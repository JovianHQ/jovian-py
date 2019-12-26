from random import random

import requests
from pkg_resources import parse_version

from jovian._version import __version__
from jovian.utils.jupyter import in_notebook
from jovian.utils.logger import log


def _get_latest_version():
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


def _print_update_message(current_version, latest_version):
    log('Update Available: {0} --> {1}'.format(current_version, latest_version))

    if in_notebook():
        log('Run `!pip install jovian --upgrade` to upgrade')
    else:
        log('Run `pip install jovian --upgrade` to upgrade\n')


def check_update(probability=0.8):
    """Check if there is a update available and logs
    current and latest version with the command to update
    the library.

    Args:
        probability (float, optional): Approximate probability with which the user
                                    is notified. Defaults to .2(~20%).
                                    (1 == always)
    """
    if random() < probability:
        latest_version = parse_version(_get_latest_version())
        current_version = parse_version(__version__)
        if latest_version > current_version:
            _print_update_message(current_version, latest_version)
