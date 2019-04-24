"""Anaconda related utilities"""
import os
import logging
from jovian.utils.api import upload_file
from jovian.utils.misc import get_platform
from jovian.utils.constants import PLATFORMS


class CondaError(Exception):
    """Error class for Anaconda-related exceptions"""
    pass


CONDA_NOT_FOUND = 'Anaconda binary not found. Please make sure the "conda" command is in your system PATH or the environment variable $CONDA_EXE points to the anaconda binary'


def get_conda_bin():
    """Get the path to the Anaconda binary"""
    conda_bin = 'conda'
    # Try executing the `conda` command
    if os.popen(conda_bin).read().strip() == '':
        # If it fails, look for $CONDA_EXE
        conda_exe = os.popen('echo $CONDA_EXE').read().strip()
        # Check if it returns a valid path
        if conda_exe != '' and conda_exe != '$CONDA_EXE':
            # Update binary and execute again
            conda_bin = conda_exe
            if os.popen(conda_bin).read().strip() == '':
                raise CondaError(CONDA_NOT_FOUND)
    logging.info('Anaconda binary: ' + conda_bin)
    return conda_bin


def get_conda_env_name():
    """Get the name of the active conda environment"""
    env_name = os.popen('echo $CONDA_DEFAULT_ENV').read().strip()
    if env_name == '' or env_name == '$CONDA_DEFAULT_ENV':
        env_name = 'base'
    logging.info('Anaconda environment: ' + env_name)
    return env_name


def read_conda_env(name=None):
    """Read the anaconda environment into a string"""
    if name is None:
        name = get_conda_env_name()
    command = get_conda_bin() + ' env export -n ' + \
        get_conda_env_name() + " --no-builds"
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
    upload_file(gist_slug, ('environment.yml', env_str))

    # Check and include existing os-specific files
    platform = get_platform()
    for p in PLATFORMS:
        pfname = 'environment-' + p + '.yml'
        if p == platform:
            # Use the new environment for current platform
            upload_file(gist_slug, (pfname, env_str), version)
        elif os.path.exists(pfname):
            # Reuse old environments for other platforms
            upload_file(gist_slug, pfname, version)
