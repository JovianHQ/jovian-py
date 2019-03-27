"""Utilities to read, write and manage the credentials file"""
import os
from getpass import getpass
import json
import stat
import shutil
import uuid
from uuid import UUID
from jovian.utils.logger import log
from jovian.utils.constants import WEBAPP_URL, API_KEY, GUEST_KEY


CREDS = {}

HOME = os.path.expanduser('~')
CONFIG_DIR = HOME + '/.jovian'
CREDS_FNAME = 'credentials.json'
CREDS_PATH = CONFIG_DIR + '/' + CREDS_FNAME


def config_exists():
    """Check if config directory exists"""
    return os.path.exists(CONFIG_DIR)


def init_config():
    """Create the config directory"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


def purge_config():
    """Remove the config directory"""
    return shutil.rmtree(CONFIG_DIR, ignore_errors=True)


def purge_creds():
    """Remove the config directory"""
    if os.path.isfile(CREDS_PATH):
        os.remove(CREDS_PATH)


def creds_exist():
    """Check if credentials file exits"""
    return os.path.exists(CREDS_PATH)


def read_creds():
    """Read the credentials file"""
    with open(CREDS_PATH, 'r') as f:
        try:
            return json.load(f)
        except ValueError:
            purge_creds()
            return {}


def write_creds(creds, update_cache=True):
    """Write the given credentials to file"""
    init_config()
    with open(CREDS_PATH, 'w') as f:
        json.dump(creds, f)
    os.chmod(CREDS_PATH, stat.S_IREAD | stat.S_IWRITE)

    if update_cache:
        _get_or_init_creds()


def _get_or_init_creds():
    global CREDS
    CREDS = read_creds() if creds_exist() else {}
    return CREDS


def _write_key(key, key_name):
    creds = _get_or_init_creds()
    if key_name in creds and creds[key_name] == key:
        return
    else:
        creds[key_name] = key
        write_creds(creds)


def write_guest_key(key):
    """Write the GUEST key to memory, and the credentials file"""
    _write_key(key, GUEST_KEY)


def write_api_key(key):
    """Write the API key to memory, and the credentials file"""
    _write_key(key, API_KEY)


def request_api_key():
    """Ask the user to provide the API key"""
    log("Please enter your API key (from " + WEBAPP_URL + " ):")
    api_key = getpass()
    return api_key


def read_api_key_opt():
    """Read credentials file, or return None"""
    creds = _get_or_init_creds()
    api_key = creds[API_KEY] if API_KEY in creds else None

    return api_key, 'read'


def read_or_request_api_key():
    """Read credentials file, or ask the user for API Key, if required"""
    api_key, source = read_api_key_opt()

    if api_key is not None:
        return api_key, source
    else:
        return request_api_key(), 'request'


def _generate_guest_key():
    """Generate GUEST key"""
    return uuid.uuid4().hex


def _read_or_generate_guest_key():
    """Read credentials file, or generate GUEST key, if required"""
    creds = _get_or_init_creds()
    return creds[GUEST_KEY] if GUEST_KEY in creds else _generate_guest_key()


def _validate_guest_key(key):
    """Validate GUEST key"""
    try:
        val = UUID(key, version=4)
    except ValueError:
        return False
    return val.hex == key


def get_guest_key():
    if GUEST_KEY not in CREDS:
        key = _read_or_generate_guest_key()
        if not _validate_guest_key(key):
            key = _generate_guest_key()
        write_guest_key(key)
        return key

    return CREDS[GUEST_KEY]
