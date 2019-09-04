from jovian.utils.credentials import creds_exist, purge_creds
from jovian.utils.logger import log
from jovian.utils.credentials import ensure_org, get_guest_key
from jovian.utils.api import get_api_key


def configure():
    """Configure Jovian for first time usage"""
    # Check if already exists
    print('Checking existence..')
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
            log('Removing existing credentials..')
            purge_creds()
        else:
            log('Skipping..')
            return

    # Capture and save organization ID
    print('Checking org details')
    ensure_org()

    # Ask for API Key
    print('Setting guest and API key')
    get_guest_key()
    get_api_key()

    log('Configuration complete!')
