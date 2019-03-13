import platform
from jovian.utils.constants import LINUX, WINDOWS, MACOS


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
