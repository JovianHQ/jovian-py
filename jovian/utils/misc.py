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
