"""Anaconda related utilities"""
import os
import logging
from jovian.utils.api import upload_file


class CondaError(Exception):
    """Error class for Anaconda-related exceptions"""
    pass


def get_conda_bin():
    """Get the path to the Anaconda binary"""
    conda_bin = os.popen('echo $CONDA_EXE').read().strip()
    if conda_bin == '' or conda_bin == '$CONDA_EXE':
        if os.popen('conda').read().strip() == '':
            raise CondaError(
                'Anaconda binary not found. Please make sure the "conda" command is in your system PATH or the environment variable $CONDA_EXE points to the anaconda binary')
        else:
            conda_bin = 'conda'
    logging.info('Anaconda binary: ' + conda_bin)
    return conda_bin


def get_conda_env_name():
    """Get the name of the active conda environment"""
    env_name = os.popen('echo $CONDA_DEFAULT_ENV').read().strip()
    if env_name == '':
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


def upload_conda_env(gist_slug):
    """Read and save the current Anaconda environment to server"""
    name = get_conda_env_name()
    env_str = read_conda_env(name)
    return upload_file(gist_slug, ('environment.yml', env_str))
