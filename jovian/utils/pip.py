"""Pip related utilities"""
import os
from jovian.utils.api import upload_file


def read_pip_env():
    """Read the pip dependencies into a string"""
    command = "pip --disable-pip-version-check freeze"
    deps_str = os.popen(command).read()
    if deps_str == '':
        error = 'Failed to read Anaconda environment using command: "' + command + '"'
        raise Exception(error)
    return deps_str


def upload_pip_env(gist_slug, version=None):
    """Read and upload the current virtual environment to server"""
    return upload_file(gist_slug, ('requirements.txt', read_pip_env(), version))
