from jovian._version import __version__
from time import sleep
from jovian.utils.anaconda import upload_conda_env
from jovian.utils.pip import upload_pip_env
from jovian.utils.api import create_gist_simple
from jovian.utils.logger import log
from jovian.utils.constants import WEBAPP_URL


def commit(capture_env=True, filename=None):
    """Save the notebook, capture the environment, and upload to cloud for sharing"""
    res = create_gist_simple(filename)
    if res is None:
        return

    slug, owner = res['slug'], res['owner']

    # Save & upload environment
    if capture_env:
        log('Capturing environment..')
        try:
            upload_conda_env(slug)
        except:
            try:
                upload_pip_env(slug)
            except:
                log('Failed to capture the Python environment', error=True)

    log('Committed successfully! ' + WEBAPP_URL +
        "/" + owner['username'] + "/" + slug)
