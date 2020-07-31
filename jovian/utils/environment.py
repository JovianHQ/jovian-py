"""Anaconda and Pip related utilities"""
import os
import logging
from jovian.utils.api import upload_file
from jovian.utils.misc import get_platform
from jovian.utils.constants import PLATFORMS, CONDA_NOT_FOUND
from jovian.utils.logger import log
from jovian.utils.error import CondaError


def get_conda_bin():
    """Get the path to the Anaconda binary"""
    conda_bin = 'conda'
    # Try executing the `conda` command
    if os.popen(conda_bin).read().strip() == '':
        # If it fails, look for $CONDA_EXE
        conda_exe = os.environ.get("CONDA_EXE")
        # Check if it returns a valid path
        if conda_exe and conda_exe != '$CONDA_EXE':
            # Update binary and execute again
            conda_bin = conda_exe
            if os.popen(conda_bin).read().strip() == '':
                raise CondaError(CONDA_NOT_FOUND)
    logging.info('Anaconda binary: ' + conda_bin)
    return conda_bin


def get_conda_env_name():
    """Get the name of the active conda environment"""
    env_name = os.environ.get("CONDA_DEFAULT_ENV", "base")
    if not env_name:
        env_name = "base"
    logging.info('Anaconda environment: ' + env_name)
    return env_name


def read_conda_env(name=None):
    """Read the anaconda environment into a string"""
    if name is None:
        name = get_conda_env_name()
    command = get_conda_bin() + ' env export -n ' + name + " --no-builds"
    env_str = os.popen(command).read()
    if env_str == '':
        error = 'Failed to read Anaconda environment using command: "' + command + '"'
        raise CondaError(error)
    return env_str


def upload_conda_env(gist_slug, version=None):
    """Read and save the current Anaconda environment to server"""
    # Export environment to YML string
    env_str = read_conda_env(get_conda_env_name())

    # Upload environment.yml
    upload_file(gist_slug=gist_slug, file=('environment.yml', env_str), version=version)

    # Check and include existing os-specific files
    platform = get_platform()
    for p in PLATFORMS:
        pfname = 'environment-' + p + '.yml'
        if p == platform:
            # Use the new environment for current platform
            upload_file(gist_slug=gist_slug, file=(pfname, env_str), version=version)
        elif os.path.exists(pfname):
            # Reuse old environments for other platforms
            with open(pfname, 'rb') as f:
                file = (pfname, f)
                upload_file(gist_slug=gist_slug, file=file, version=version)


def print_conda_message(env_name):
    if env_name:
        message = ("""
#
# To activate this environment, use
#
#     $ conda activate %s
#
# To deactivate an active environment, use
#
#     $ conda deactivate
        """) % env_name
        log(message)


def read_pip_env():
    """Read the pip dependencies into a string"""
    command = "pip --disable-pip-version-check freeze"
    deps_str = os.popen(command).read()
    if deps_str == '':
        error = 'Failed to read pip environment using command: "' + command + '"'
        raise Exception(error)
    return deps_str


def upload_pip_env(gist_slug, version=None):
    """Read and upload the current virtual environment to server"""
    return upload_file(gist_slug=gist_slug, file=('requirements.txt', read_pip_env()), version=version)
