"""Utilities to read, write and manage the credentials file"""
import os
from getpass import getpass
import json
import stat
import shutil
import uuid
import requests
from uuid import UUID
from jovian.utils.logger import log
from jovian.utils.misc import is_flavor_pro
from jovian.utils.constants import DEFAULT_API_URL, DEFAULT_WEBAPP_URL


try:
    # Python 3
    from json.decoder import JSONDecodeError
except ImportError:
    # Python 2
    JSONDecodeError = ValueError


# Keys used in credentials file
API_TOKEN_KEY = "API_KEY"
GUEST_TOKEN_KEY = "GUEST_KEY"
ORG_ID_KEY = "ORG_ID"
API_URL_KEY = "API_URL"
WEBAPP_URL_KEY = "WEBAPP_URL"

# Paths and filenames
HOME = os.path.expanduser('~')
CONFIG_DIR = HOME + '/.jovian'
CREDS_FNAME = 'credentials.json'
CREDS_PATH = CONFIG_DIR + '/' + CREDS_FNAME

CONTACT_MSG = 'Looks like there\'s something wrong with your setup. Please report this issue to hello@jvn.io .'


class ConfigError(Exception):
    """Error class for config related Exceptions"""
    pass


# Config directory management

def config_exists():
    """Check if config directory exists"""
    return os.path.exists(CONFIG_DIR)


def purge_config():
    """Remove the config directory"""
    return shutil.rmtree(CONFIG_DIR, ignore_errors=True)


def init_config():
    """Create the config directory"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)


# Credentials file management

def purge_creds():
    """Remove the credentials file"""
    if os.path.isfile(CREDS_PATH):
        os.remove(CREDS_PATH)


def read_creds():
    """Read the credentials file"""
    if not os.path.exists(CREDS_PATH):
        return {}
    with open(CREDS_PATH, 'r') as f:
        try:
            return json.load(f)
        except ValueError:
            purge_creds()
            return {}


def creds_exist():
    """Check if credentials file exits"""
    creds = read_creds()
    return API_TOKEN_KEY in creds


def read_cred(key, default=None):
    """Read a particular key from the credentials file"""
    creds = read_creds()
    if default:
        return creds.get(key, default)
    return creds[key]


def write_creds(creds, update_cache=True):
    """Write the given credentials to file"""
    init_config()
    with open(CREDS_PATH, 'w') as f:
        json.dump(creds, f)
    os.chmod(CREDS_PATH, stat.S_IREAD | stat.S_IWRITE)


def write_cred(key, value):
    creds = read_creds()
    if key in creds and creds[key] == value:
        return
    creds[key] = value
    write_creds(creds)


# API URL

def write_api_url(value):
    """Write the API URL"""
    write_cred(API_URL_KEY, value)


def read_api_url():
    ensure_org()
    return read_cred(API_URL_KEY, DEFAULT_API_URL)


# Webapp URL

def write_webapp_url(value):
    """Write the webapp URL"""
    write_cred(WEBAPP_URL_KEY, value)


def read_webapp_url():
    """Read the webapp URL"""
    ensure_org()
    return read_cred(WEBAPP_URL_KEY, DEFAULT_WEBAPP_URL)


# Organization ID

def write_org_id(value):
    """Write the Organization ID"""
    write_cred(ORG_ID_KEY, value)


def request_org_id():
    """Ask the user to provide the organization ID"""
    log("If you're a jovian-pro user please enter your company's organization ID on Jovian (otherwise leave it blank).")
    msg = "Organization ID:"
    try:
        user_input = raw_input(msg)
    except NameError:
        try:
            user_input = input(msg)
        except EOFError:
            user_input = ''
    return user_input


def read_org_id():
    """Read Organization ID"""
    ensure_org()
    return read_cred(ORG_ID_KEY, '')


def ensure_org(check_pro=True):
    # Check the flavor
    if check_pro and not is_flavor_pro():
        return

    # Read the credentials
    creds = read_creds()
    try:
        org_id = creds[ORG_ID_KEY]
        api_url = creds[API_URL_KEY]
        webapp_url = creds[WEBAPP_URL_KEY]
        if org_id and api_url and webapp_url:
            return
    except KeyError:
        pass

    # Request organization
    org_id = request_org_id()

    # Construct the webapp URL
    if org_id:
        webapp_url = 'https://' + org_id + '.jvn.io/'
    else:
        org_id = 'public'
        webapp_url = 'https://jvn.io/'

    # Try to retrieve the config.json file from webapp
    try:
        config_url = webapp_url + 'config.json'
        config_res = requests.get(config_url)
    except ConnectionError as e:
        msg = 'Failed to connect to ' + webapp_url + \
            ' . Please verify your organization ID and ensure you are connected to the internet.'
        log(msg, error=True)
        raise ConfigError(msg, e)

    # Check for a successful response
    if config_res.status_code != 200:
        msg = 'Request to retrieve configuration file ' + config_url + \
            ' failed with status_code ' + config_res.status_code + ' . ' + CONTACT_MSG
        log(msg, error=True)
        raise ConfigError(msg + ' Response (truncated):\n' +
                          config_res.text[:100])

    # Parse JSON configuration
    try:
        config_json = config_res.json()
    except JSONDecodeError as e:
        msg = 'Failed to parse JSON configuration file from ' + \
            config_url + ' . ' + CONTACT_MSG
        log(msg, error=True)
        raise ConfigError(msg + ' Response (truncated):\n' +
                          config_res.text[:100], e)

    # Extract API URL
    try:
        api_url = config_json[API_URL_KEY]
    except KeyError:
        msg = 'Failed to extract API_URL from JSON configuration file ' + \
            config_url + ' . ' + CONTACT_MSG
        log(msg, error=True)
        raise ConfigError(msg, e)

    # Save details to credentials file
    write_org_id(org_id)
    write_api_url(api_url)
    write_webapp_url(webapp_url)


def write_api_key(value):
    """Write the API key to memory, and the credentials file"""
    write_cred(API_TOKEN_KEY, value)


# Guest token

def write_guest_key(token):
    """Write the GUEST key to memory, and the credentials file"""
    write_cred(GUEST_TOKEN_KEY, token)


def request_api_key():
    """Ask the user to provide the API key"""
    log("Please enter your API key ( from " + read_webapp_url() + " ):")
    api_key = getpass(prompt="API Key:")
    return api_key


def read_api_key_opt():
    """Read credentials file, or return None"""
    creds = read_creds()
    return creds.get(API_TOKEN_KEY), 'read'


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
    creds = read_creds()
    return creds.get(GUEST_TOKEN_KEY, _generate_guest_key())


def _validate_guest_key(key):
    """Validate GUEST key"""
    try:
        val = UUID(key, version=4)
    except ValueError:
        return False
    return val.hex == key


def get_guest_key():
    """Retrieve or generate the guest key"""
    # Read credentials
    creds = read_creds()
    guest_key = creds.get(GUEST_TOKEN_KEY, '')
    # Check validity & generate key (if required)
    if not _validate_guest_key(guest_key):
        write_cred(GUEST_TOKEN_KEY, _generate_guest_key())
        creds = read_creds()
    # Return final key
    return creds[GUEST_TOKEN_KEY]
