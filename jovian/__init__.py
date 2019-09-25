import os
from os.path import basename
from jovian._version import __version__
from time import sleep
from jovian.utils.anaconda import upload_conda_env, CondaError
from jovian.utils.pip import upload_pip_env
from jovian.utils.api import (create_gist_simple, upload_file, get_gist_access,
                              post_block, commit_records, post_slack_message, get_gist)
from jovian.utils.logger import log
from jovian.utils.constants import FILENAME_MSG, RC_FILENAME
from jovian.utils.jupyter import set_notebook_name, in_notebook, save_notebook, get_notebook_name
from jovian.utils.rcfile import get_notebook_slug, set_notebook_slug, make_rcdata
from jovian.utils.misc import get_flavor
from jovian.utils.credentials import read_webapp_url
from jovian.utils.configure import configure, reset as reset_config

__flavor__ = get_flavor()

set_notebook_name()

_current_slug = None
_data_blocks = []


def reset():
    """Reset the tracked hyperparameters & metrics (for a fresh experiment)"""
    global _current_slug
    global _data_blocks
    _current_slug = None
    _data_blocks = []


def commit(secret=False, nb_filename=None, files=[], capture_env=True,
           env_type='conda', notebook_id=None, create_new=None, artifacts=[]):
    """Commits a Jupyter Notebook with its environment to Jovian.

    Saves the checkpoint of the notebook, captures the required dependencies from 
    the python environment and uploads the notebook, env file, additional files like scripts, csv etc.
    to `Jovian`_. Capturing the python environment ensures that the notebook can be reproduced.

    Args:
        secret(bool, optional): Create a secret notebook on Jovian, which is only
            accessible via the link, and is not visible on the owner's public profile. By default,
            committed notebooks are public and visible on the owner's profile.

        nb_filename(string, optional): The filename of the jupyter notebook(including
            the .ipynb extension). This is detected automatically in most cases, but in
            certain environments like Jupyter Lab, the detection may fail and the filename
            needs to be provided using this argument.

        files(array, optional): Any additional scripts(.py files), CSVs that are required to
            run the notebook. These will be available in the files tab on Jovian .

        capture_env(bool, optional): If `True`, the Python environment(python version,
            libraries etc.) are captured and uploaded along with the notebook.

        env_type(string, optional): The type of environment to be captured. Allowed options are
            'conda' and 'pip'.

        notebook_id(string, optional): If you wish to update an existing notebook owned by you,
            you can use this argument to provide the base64 ID(present in the URL) of an notebook
            hosted on Jovian . In most cases, this argument is not required, and the library
            can automatically infer whether you are looking to update an existing notebook or create
            a new one.

        create_new(bool, optional): If set to True, doesn't update the existing notebook on
            Jovian(if one is detected). Instead, it creates a new notebook when commit is called.

        artifacts(array, optional): Any outputs files or artifacts generated from the modeling processing.
            This can include model weights/checkpoints, generated CSVs, images etc.

    .. attention::
        Pass notebook's name to nb_filename argument, in certain environments like Jupyter Lab and password protected notebooks sometimes it may fail to detect notebook automatically.
    .. _Jovian: https://jovian.ml
    """
    global _current_slug
    global _data_blocks

    # Check if we're in a Jupyter environment
    if not in_notebook():
        log('Failed to detect Juptyer notebook. Skipping..', error=True)
        return

    # Save the notebook (uses Javascript, doesn't work everywhere)
    log('Saving notebook..')
    save_notebook()
    sleep(1)

    # Get the filename of the notebook (if not provided)
    if nb_filename is None:
        nb_filename = get_notebook_name()

    # Exit with help message if filename wasn't detected (or provided)
    if nb_filename is None:
        log(FILENAME_MSG)
        return

    # Check whether to create a new gist, or update an old one
    if not create_new and notebook_id is None:
        # First preference to the in-memory slug variable
        if _current_slug is not None:
            notebook_id = _current_slug
        else:
            notebook_id = get_notebook_slug(nb_filename)

    # Check if notebook exists is a uuid or 'username/title'
    if notebok_id is not None and '/' in notebook_id:
        notebook_id = get_gist(notebook_id)['slug']

    # Check if the current user can push to this slug
    if notebook_id is not None:
        gist_access = get_gist_access(notebook_id)
        if not gist_access['write']:
            notebook_id = None

    # Log whether this is an update or creation
    if notebook_id is None:
        log('Creating a new notebook on ' + read_webapp_url())
    else:
        log('Updating notebook "' + notebook_id + '" on ' + read_webapp_url())

    # Upload the notebook & create/update the gist
    res = create_gist_simple(nb_filename, notebook_id, secret)
    if res is None:
        return

    # Extract slug and owner from created gist
    slug, owner, version = res['slug'], res['owner'], res['version']

    # Set/update the slug information
    _current_slug = slug
    set_notebook_slug(nb_filename, slug)

    # Save & upload environment
    if capture_env:
        log('Capturing environment..')

        if env_type == 'conda':
            # Capture conda environment
            try:
                upload_conda_env(gist_slug=slug, version=version)
            except CondaError as e:
                log(str(e), error=True)

        elif env_type == 'pip':
            # Capture pip environment
            try:
                upload_pip_env(gist_slug=slug, version=version)
            except Exception as e:
                log(str(e), error=True)

    # Upload additional files
    if files and len(files) > 0:
        log('Uploading additional files..')

        # Upload each file
        for fname in files:
            if os.path.exists(fname) and not os.path.isdir(fname):
                try:
                    with open(fname, 'rb') as f:
                        file = (basename(fname), f)
                        upload_file(gist_slug=slug, file=file, version=version)
                except Exception as e:
                    log(str(e), error=True)
            elif os.path.isdir(fname):
                log('Ignoring directory "' + fname + '"', error=True)
            else:
                log('Ignoring "' + fname + '" (not found)', error=True)

    # Upload artifacts
    if artifacts and len(artifacts) > 0:
        log('Uploading artifacts..')

        # Upload each artifact
        for fname in artifacts:
            if os.path.exists(fname) and not os.path.isdir(fname):
                try:
                    with open(fname, 'rb') as f:
                        file = (basename(fname), f)
                        upload_file(gist_slug=slug, file=file,
                                    version=version, artifact=True)
                except Exception as e:
                    log(str(e), error=True)
            elif os.path.isdir(fname):
                log('Ignoring directory "' + fname +
                    '". Please include files directly', error=True)
            else:
                log('Ignoring "' + fname + '" (not found)', error=True)

    # Record metrics & hyperparameters
    if len(_data_blocks) > 0:
        log('Recording metrics & hyperparameters..')
        commit_records(slug, _data_blocks, version)

    # Print commit URL
    log('Committed successfully! ' + read_webapp_url() +
        owner['username'] + "/" + slug)


def log_hyperparams(data, verbose=True):
    """Record hyperparameters for the current experiment

    Args:
        data(dict): A python dict or a array of dicts to be recorded as hyperparmeters.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove this by setting the argument to False.

    Example
        .. code-block::

            import jovian

            hyperparams = {
                'arch_name': 'cnn_1',
                'lr': .001
            }
            jovian.log_hyperparams(hyperparams)
    """
    global _data_blocks
    res = post_block(data, 'hyperparams')
    _data_blocks.append(res['tracking']['trackingSlug'])
    if verbose:
        log('Hyperparameters logged.')


def log_metrics(data, verbose=True):
    """Record metrics for the current experiment

    Args:
        data(dict): A python dict or a array of dicts to be recorded as metrics.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove this by setting the argument to False.

    Example
        .. code-block::

            import jovian

            metrics = {
                'epoch': 1,
                'train_loss': .5,
                'val_loss': .3,
                'acc': .94
            }
            jovian.log_metrics(metrics)
    """
    global _data_blocks
    res = post_block(data, 'metrics')
    _data_blocks.append(res['tracking']['trackingSlug'])
    if verbose:
        log('Metrics logged.')


def log_dataset(data, verbose=True):
    """Record dataset details for the current experiment

    Args:
        data(dict): A python dict or a array of dicts to be recorded as Dataset.

        verbose(bool, optional): By default it prints the acknowledgement, you can remove this by setting the argument to False.

    Example
        .. code-block::

            import jovian

            data = {
                'path': '/datasets/mnist',
                'description': '28x28 images of handwritten digits (in grayscale)'
            }
            jovian.log_dataset(data)
    """
    global _data_blocks
    res = post_block(data, 'dataset')
    _data_blocks.append(res['tracking']['trackingSlug'])
    if verbose:
        log('Dataset logged.')


def notify(data, verbose=True, safe=False):
    """Sends the data to the `Slack`_ workspace connected with your `Jovian`_ account.

    Args:
        data(dict|string): A dict or string to be pushed to Slack

        verbose(bool, optional): By default it prints the acknowledgement, you can remove this by setting the argument to False.

        safe(bool, optional): To avoid raising ApiError exception. Defaults to False.

    Example
        .. code-block::

            import jovian

            data = "Hello from the Integration!"
            jovian.notify(data)

    .. important::
        This feature requires for your Jovian account to be connected to a Slack workspace, visit `Jovian Integrations`_ to integrate them and to control the type of notifications.
    .. _Slack: https://slack.com
    .. _Jovian: https://jovian.ml
    .. _Jovian Integrations: https://jovian.ml/settings/integrations
    """
    res = post_slack_message(data=data, safe=safe)
    if verbose:
        if not res.get('errors'):
            log('message_sent:' + str(res.get('data').get('messageSent')))
        else:
            log(str(res.get('errors')[0].get('message')), error=True)
