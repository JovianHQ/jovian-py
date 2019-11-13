import requests
from random import random

from jovian._version import __version__
from jovian.utils.logger import log


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


def notify():
    """Log Update available with current, latest version and command to upgrade.
    """
    latest_version = get_latest_version()
    if latest_version > __version__:
        log('Update Available: {0} --> {1}'.format(__version__, latest_version))
        log('Run `!pip install jovian --upgrade` to upgrade')


def random_notify():
    """Notifies randomly if update is available.
    """
    if random() < .2:
        notify()
