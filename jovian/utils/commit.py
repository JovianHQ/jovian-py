import os
from time import sleep

from jovian.utils.script import in_script, get_script_filename
from jovian.utils.jupyter import in_notebook, get_notebook_name, save_notebook
from jovian.utils.misc import get_file_extension, is_uuid
from jovian.utils.rcfile import get_notebook_slug, set_notebook_slug
from jovian.utils.credentials import read_webapp_url
from jovian.utils.environment import upload_conda_env, CondaError, upload_pip_env
from jovian.utils.records import log_git, get_records, reset
from jovian.utils.constants import FILENAME_MSG
from jovian.utils.logger import log
from jovian.utils import api, git

_current_slug = None


def commit(message=None,
           files=[],
           outputs=[],
           environment='auto',
           privacy='auto',
           filename=None,
           project=None,
           new_project=None,
           git_commit=True,
           git_message='auto',
           **kwargs):
    """Uploads the current file (Jupyter notebook or python script) to |Jovian|

    Saves the checkpoint of the notebook, captures the required dependencies from 
    the python environment and uploads the notebook, env file, additional files like scripts, csv etc.
    to |Jovian|. Capturing the python environment ensures that the notebook can be reproduced.

    Args:
        message(string, optional): A short message to be used as the title for this version.

        files(array, optional): Any additional scripts(.py files), CSVs etc. that are required to
            run the notebook. These will be available in the files tab of the project page on Jovian.ml

        outputs(array, optional): Any outputs files or artifacts generated from the modeling processing.
            This can include model weights/checkpoints, generated CSVs, output images etc.

        environment(string, optional): The type of Python environment to be captured.  Allowed options are
            'conda' , 'pip', 'auto' (for automatic detection) and None (to skip environment capture).

        privacy(bool, optional): Privacy level of the project (if a new one is being created).

            * 'auto' - use account level settings. Defaults to 'public'
            * 'public' - visible on profile and publicly accessible/searchable
            * 'secret' - not on profile only accessible via the direct link
            * 'private' - only for the accessible to owner and collaborators

            This argument has no effect on existing project. Change the privacy settings of a existing notebook 
            on the webapp.

        filename(string, optional): The filename of the current Jupyter notebook or Python script. This is 
            detected automatically in most cases, but in certain environments like Jupyter Lab or password protected notebooks, the detection 
            may fail and the filename needs to be provided using this argument.


        project(string, optional): Name of the |Jovian| project to which the current notebook/file should 
            be committed. Format: 'username/title' e.g. 'aakashns/jovian-example' or 'jovian-example' 
            (username of current user inferred automatically). If the project does not exist, a new one is 
            created. If it exists, the current notebook is added as a new version to the existing project, if 
            you are a owner/collaborator. If left empty, project name is picked up from the `.jovianrc` file in the 
            current directory, or a new project is created using the filename as the project name. 

        new_project(bool, optional): Whether to create a new project or update the existing one. Allowed option 
            are False (use the existing project, if a .jovianrc file exists, if available), True (create a new project)

        git_commit(bool, optional): If True, also performs a Git commit and records the commit hash. This is 
            applicable only when the notebook is inside a Git repository.

        git_message(string, optional): Commit message for git. If not provided, it uses the `message` argument

    .. attention::
        Pass notebook's name to `filename` argument, in certain environments like Jupyter Lab and password protected 
        notebooks sometimes it may fail to detect notebook automatically.
    .. |Jovian| raw:: html

        <a href="https://jovian.ml/?utm_source=docs" target="_blank"> Jovian.ml </a>
    """
    global _current_slug

    # Deprecated argument (secret)
    if privacy == 'auto' and 'secret' in kwargs:
        privacy = 'secret' if kwargs['secret'] else 'auto'
        log('"secret" is deprecated. Use "privacy" instead (allowed options: ' +
            '"public", "private", "secret", "auto")', error=True)

    # Deprecated argument (nb_filename)
    if filename is None and 'nb_filename' in kwargs:
        filename = kwargs['nb_filename']
        log('"nb_filename" is deprecated. Use "filename" instead', error=True)

    # Deprecated argument (env_type)
    if 'env_type' in kwargs:
        environment = kwargs['environment']
        log('"env_type" is deprecated. Use "environment" instead', error=True)

    # Deprecated argument (capture_env)
    if 'capture_env' in kwargs and not kwargs['capture_env']:
        environment = None
        log('"catpure_env" is deprecated. Use "environment=None" instead', error=True)

    # Deprecated argument (notebook_id)
    if 'notebook_id' in kwargs:
        project = kwargs['notebook_id']
        log('"notebook_id" is deprecated. Use "project" instead.', error=True)

    # Deprecated argument (create_new)
    if 'create_new' in kwargs:
        new_project = kwargs['create_new']
        log('"create_new" is deprecated. Use "new_project" instead.', error=True)

    # Deprecated argument (artifacts)
    if 'artifacts' in kwargs:
        outputs = kwargs['artifacts']
        log('"artifacts" is deprecated. Use "outputs" instead', error=True)

    # Skip if unsupported environment
    if not in_script() and not in_notebook():
        log('Failed to detect Jupyter notebook or Python script. Skipping..', error=True)
        return

    # Attempt to save Jupyter notebook
    if in_notebook():
        save_notebook()
        log('Attempting to save notebook..')
        sleep(1)

    # Extract notebook/script filename
    filename = _parse_filename(filename)
    if filename is None:
        log(FILENAME_MSG)
        return

    # Ensure that the file exists
    if not os.path.exists(filename):
        log('The detected/provided file "' + filename +
            '" does not exist. Please provide the correct notebook filename ' +
            'as the "filename" argument to "jovian.commit".')
        return

    # Retrieve Gist ID & title
    project_title, project_id = _parse_project(project, filename, new_project)

    # Create or update gist (with title and )
    res = api.create_gist_simple(filename, project_id, privacy, project_title, message)
    slug, owner, version, title = res['slug'], res['owner'], res['version'], res['title']
    username = owner['username']

    # Cache slug for further commits
    _current_slug = slug
    set_notebook_slug(filename, slug)

    # Attach environment, files and outputs
    _capture_environment(environment, slug, version)
    _attach_files(files, slug, version)
    _attach_files(outputs, slug, version, output=True)

    if not git_message or git_message == 'auto':
        git_message = message or 'jovian commit ' + username + '/' + title + ' v' + str(version)
    _perform_git_commit(filename, git_commit, git_message)
    _attach_records(slug, version)

    log('Committed successfully! ' + read_webapp_url() + username + "/" + title)


def _parse_filename(filename):
    """Perform the required checks and get the final filename"""
    # Get the filename of the notebook (if not provided)
    if filename is None:
        if in_script():
            filename = get_script_filename()
        elif in_notebook():
            filename = get_notebook_name()

    # Add the right extension to the filename
    elif get_file_extension(filename) not in ['.py', '.ipynb']:
        filename += '.py' if in_script() else '.ipynb'
    return filename


def _parse_project(project, filename, new_project):
    """Perform the required checks and get the final project name"""
    global _current_slug

    # Check for existing project in-memory or in .jovianrc
    if not new_project and project is None:
        # From in-memory variable
        if _current_slug is not None:
            project = _current_slug
        # From .jovianrc file
        else:
            project = get_notebook_slug(filename)

    # Skip if project is not provided & can't be read
    if project is None:
        return None, None

    # Get project metadata for UUID & username/title
    if is_uuid(project):
        project_title = None
        metadata = api.get_gist(project)
    elif '/' in project:
        project_title = project.split('/')[1]
        metadata = api.get_gist(project)
    # Attach username to the title
    else:
        project_title = project
        username = api.get_current_user()['username']
        metadata = api.get_gist(username + '/' + project)

    # Skip if metadata could not be found
    if not metadata:
        log('Creating a new project "' + username + '/' + project + '"')
        return project_title, None

    # Extract information from metadata
    username = metadata['owner']['username']
    project_title = metadata['title']
    project_id = metadata['slug']

    # Check if the current user can commit to this project
    permissions = api.get_gist_access(project_id)
    if not permissions['write']:
        return project_title, None

    # Log whether this is an update or creation
    if project_id is None:
        log('Creating a new notebook on ' + read_webapp_url())
    else:
        log('Updating notebook "' + username + "/" + project_title + '" on ' + read_webapp_url())

    return project_title, project_id


def _attach_file(path, gist_slug, version, output=False):
    """Helper function to attach a single file to a commit"""
    try:
        with open(path, 'rb') as f:
            file_obj = os.path.basename(path), f
            folder = os.path.dirname(path)
            api.upload_file(gist_slug, file_obj, folder, version, output)
    except Exception as e:
        log(str(e) + " (" + path + ")", error=True)


def _attach_files(paths, gist_slug, version, output=False):
    """Helper functions to attach files & folders to a commit"""
    # Skip if empty
    if not paths or len(paths) == 0:
        return

    log('Uploading additional ' + ('outputs' if output else 'files') + '...')

    # Convert single path to list
    if type(paths) == str:
        paths = [paths]

    for path in paths:
        if os.path.isdir(path):
            for folder, _, files in os.walk(path):
                for fname in files:
                    fpath = os.path.join(folder, fname)
                    _attach_file(fpath, gist_slug, version, output)
        elif os.path.exists(path):
            _attach_file(path, gist_slug, version, output)
        else:
            log('Ignoring "' + path + '" (not found)', error=True)


def _capture_environment(environment, gist_slug, version):
    """Capture the python environment and attach it to the commit"""
    if environment is not None:
        log('Capturing environment..')
        captured = False

        if environment == 'auto' or environment == 'conda':
            # Capture conda environment
            try:
                upload_conda_env(gist_slug, version)
                captured = True
            except CondaError as e:
                log(str(e), error=True)

        if not captured and (environment == 'pip' or environment == 'auto'):
            # Capture pip environment
            try:
                upload_pip_env(gist_slug, version)
            except Exception as e:
                log(str(e), error=True)


def _perform_git_commit(filename, git_commit, git_message):
    if git_commit and git.is_git():
        reset('git')  # resets git commit info

        git.commit(git_message)
        log('Git repository identified. Performing git commit...')

        git_info = {
            'repository': git.get_remote(),
            'commit': git.get_current_commit(),
            'filename': filename,
            'path': git.get_relative_path(),
            'branch': git.get_branch()
        }
        log_git(git_info, verbose=False)


def _attach_records(gist_slug, version):
    """Attached records to the current commit"""
    tracking_slugs = get_records(slug_only=True)
    if len(tracking_slugs) > 0:
        log('Attaching records (metrics, hyperparameters, dataset etc.)')
        api.post_records(gist_slug, tracking_slugs, version)
