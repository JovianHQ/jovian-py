import click

from jovian.utils.api import get_api_key
from jovian.utils.credentials import creds_exist, ensure_org, get_guest_key, purge_creds
from jovian.utils.logger import log


def reset_config(confirm=True):
    """Remove the existing configuration by purging credentials"""
    if creds_exist():
        if confirm:
            msg = 'Do you want to remove the existing configuration?'
            confirmed = click.confirm(msg)
        else:
            confirmed = True

        if confirmed:
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
        msg = 'Do you want to overwrite the existing configuration?'
        confirm = click.confirm(msg)

        if confirm:
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
