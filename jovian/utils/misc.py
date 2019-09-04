import platform
from jovian.utils.constants import LINUX, WINDOWS, MACOS
import time


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
