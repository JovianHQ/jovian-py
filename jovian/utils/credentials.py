"""Utilities to read, write and manage the credentials file"""
import os
from getpass import getpass
import json
import stat
import shutil
from jovian.utils.logger import log
from jovian.utils.constants import WEBAPP_URL

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


def creds_exist():
    """Check if credentials file exits"""
    return os.path.exists(CREDS_PATH)


def read_creds():
    """Read the credentials file"""
    with open(CREDS_PATH, 'r') as f:
        return json.load(f)


def write_creds(creds):
    """Write the given credentials to file"""
    init_config()
    with open(CREDS_PATH, 'w') as f:
        json.dump(creds, f)
    os.chmod(CREDS_PATH, stat.S_IREAD | stat.S_IWRITE)


def write_key(key, write_to_file=True):
    """Write the API key to memory, and the credentials file"""
    global CREDS
    CREDS['API_KEY'] = key
    if write_to_file:
        write_creds(CREDS)


def request_key():
    """Ask the user to provide the API key"""
    log("Please enter your API key (from " + WEBAPP_URL + " ):")
    api_key = getpass()
    return api_key


def read_or_request_key():
    """Read credentials file, and ask the user for API Key, if required"""
    if creds_exist():
        return read_creds()['API_KEY'], 'read'
    else:
        return request_key(), 'request'
