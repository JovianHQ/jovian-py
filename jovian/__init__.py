from jovian._version import __version__
from time import sleep
from jovian.utils.anaconda import upload_conda_env, CondaError
from jovian.utils.pip import upload_pip_env
from jovian.utils.api import create_gist_simple, upload_file, get_gist
from jovian.utils.logger import log
from jovian.utils.constants import WEBAPP_URL, FILENAME_MSG, RC_FILENAME
from jovian.utils.jupyter import set_notebook_name, in_notebook, save_notebook, get_notebook_name
from jovian.utils.rcfile import get_notebook_slug, set_notebook_slug, make_rcdata

set_notebook_name()

_current_slug = None


def commit(notebook_id=None, capture_env=True, filename=None, env_type='conda'):
    """Save the notebook, capture the environment, and upload to cloud for sharing"""
    global _current_slug

    # Check if we're in a Jupyter environment
    if not in_notebook():
        log('Failed to detect Juptyer notebook. Skipping..', error=True)
        return

    # Save the notebook (uses Javascript, doesn't work everywhere)
    log('Saving notebook..')
    save_notebook()
    sleep(1)

    # Get the filename of the notebook (if not provided)
    if filename is None:
        filename = get_notebook_name()

    # Exit with help message if filename wasn't detected (or provided)
    if filename is None:
        log(FILENAME_MSG)
        return

    # Check whether to create a new gist, or update an old one
    if notebook_id is None:
        # First preference to the in-memory slug variable
        if _current_slug is not None:
            notebook_id = _current_slug
        else:
            notebook_id = get_notebook_slug(filename)

    # Check if the current user can push to this slug
    if notebook_id is not None:
        gist_meta = get_gist(notebook_id)
        if not gist_meta['isOwner']:
            notebook_id = None

    # Log whether this is an update or creation
    if notebook_id is None:
        log('Creating a new notebook on https://jvn.io')
    else:
        log('Updating notebook "' + notebook_id + '" on https://jvn.io')

    # Upload the notebook & create/update the gist
    res = create_gist_simple(filename, notebook_id)
    if res is None:
        return

    # Extract slug and owner from created gist
    slug, owner = res['slug'], res['owner']

    # Set/update the slug information
    _current_slug = slug
    set_notebook_slug(filename, slug)

    # Save & upload environment
    if capture_env:
        log('Capturing environment..')

        if env_type == 'conda':
            # Capture conda environment
            try:
                upload_conda_env(slug)
            except CondaError as e:
                log(str(e), error=True)

        elif env_type == 'pip':
            # Capture pip environment
            try:
                upload_pip_env(slug)
            except Exception as e:
                log(str(e), error=True)

    # Print commit URL
    log('Committed successfully! ' + WEBAPP_URL +
        "/" + owner['username'] + "/" + slug)
