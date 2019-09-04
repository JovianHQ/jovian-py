from jovian.utils.credentials import creds_exist, purge_creds
from jovian.utils.logger import log
from jovian.utils.credentials import ensure_org, get_guest_key
from jovian.utils.api import get_api_key


def reset():
    if creds_exist():
        msg = 'Do you want to remove the existing configuration? (y/N):'
        try:
            user_input = raw_input(msg)
        except NameError:
            try:
                user_input = input(msg)
            except EOFError:
                user_input = ''
        if user_input == 'y' or user_input == 'Y':
            log('Removing existing configuration. Run "jovian configure" to set up Jovian')
            purge_creds()
        else:
            log('Skipping..')
            return
    else:
        log('Jovian is not configured yet. Run "jovian configure" to set it up.')


def configure():
    """Configure Jovian for first time usage"""
    # Check if already exists
    if creds_exist():
        log('It looks like Jovian is already configured ( check ~/.jovian/credentials.json ).')
        msg = 'Do you want to overwrite the existing configuration? (y/N):'
        try:
            user_input = raw_input(msg)
        except NameError:
            try:
                user_input = input(msg)
            except EOFError:
                user_input = ''
        if user_input == 'y' or user_input == 'Y':
            log('Removing existing configuration..')
        else:
            log('Skipping..')
            return

    # Remove existing credentials
    purge_creds()

    # Capture and save organization ID
    ensure_org(check_pro=False)

    # Ask for API Key
    get_guest_key()
    get_api_key()

    log('Configuration complete!')
