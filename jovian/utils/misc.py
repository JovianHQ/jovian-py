import os
import sys
import time
import platform

from uuid import UUID
from jovian.utils.constants import LINUX, WINDOWS, MACOS
from jovian._version import __version__


def is_uuid(text):
    """Check if the given string is a UUID"""
    try:
        _ = UUID(text, version=4)
        return True
    except ValueError:
        return False


def is_py2():
    """Check if current Python version is 2.x"""
    return sys.version_info[0] < 3


def get_platform():
    """Identify which OS the library is running on

    Returns 'linux', 'windows' or 'macos'
    """
    system = platform.system()
    if system == 'Linux':
        return LINUX
    elif system == 'Windows':
        return WINDOWS
    elif system == 'Darwin':
        return MACOS


def timestamp_ms():
    """Return the current timestamp (in milliseconds)"""
    return int(time.time() * 1000)


def get_flavor():
    """Get the flavor of the library (jovian or jovian-pro)"""
    try:
        from jovian._flavor import __flavor__
        return __flavor__
    except ImportError:
        return "jovian"


def is_flavor_pro():
    """Get the flavor of the library (jovian or jovian-pro)"""
    return get_flavor() == 'jovian-pro' or get_flavor() == 'jovianpro'


def get_file_extension(filename):
    """Get the extension of a file"""
    return os.path.splitext(filename)[1]


def urljoin(*args):
    """Join multiple url parts to construct one url"""
    if len(args) == 0:
        raise TypeError("urljoin requires at least one argument")

    trailing_slash = '/' if args[-1].endswith('/') else ''

    return '/'.join(map(lambda x: str(x).strip('/'), args)) + trailing_slash


def version():
    return __version__
