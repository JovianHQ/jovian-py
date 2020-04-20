from unittest import TestCase, mock
from unittest.mock import ANY
import pytest

from jovian.tests.resources.shared import fake_creds, MockResponse
from jovian.utils.configure import configure, reset_config
from jovian.utils.credentials import creds_exist, purge_creds, read_creds


def mock_request_get(*args, **kwargs):
    return MockResponse({
        "CONFIG_NAME": "staging",
        "APP_NAME": "Jovian (Staging)",
        "APP_DESCRIPTION": "Share Jupyter notebooks instantly",
        "IS_PRODUCTION": True,
        "IS_FLAVOR_PRO": False,
        "COMPANY_LOGO_URL": "https://i.imgur.com/iOPEHyK.png",
        "API_URL": "https://api-staging.jovian.ai",
        "API_URL_ALT": "https://staging.jovian.ml/api",
        "AUTH_ENV": "staging",
        "LOGIN_REDIRECT_PATH": "/login",
        "SEGMENT_KEY": "uMgCwYBVCuaCMGPCMWSaWLpkjgFhkyg5"
    }, 200)


@mock.patch("click.confirm", return_value=True)
def test_reset_config_prompt_confirmation(mock_confirm, capsys):
    with fake_creds('.jovian', 'credentials.json'):
        reset_config()
        assert creds_exist() == False

        expected_result = "[jovian] Removing existing configuration. Run \"jovian configure\" to set up Jovian"
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


def test_reset_config_no_prompt_confirmation(capsys):
    with fake_creds('.jovian', 'credentials.json'):
        reset_config(confirm=False)
        assert creds_exist() == False

        expected_result = "[jovian] Removing existing configuration. Run \"jovian configure\" to set up Jovian"
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@mock.patch("click.confirm", return_value=False)
def test_reset_config_confirm_false(mock_confirm, capsys):
    with fake_creds('.jovian', 'credentials.json'):
        reset_config()

        expected_result = "[jovian] Skipping.."
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


def test_reset_config_no_creds(capsys):
    with fake_creds('.jovian', 'credentials.json'):
        purge_creds()

        reset_config()

        expected_result = "[jovian] Jovian is not configured yet. Run \"jovian configure\" to set it up."
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@mock.patch("requests.get", side_effect=mock_request_get)
@mock.patch("jovian.utils.credentials.validate_api_key", return_value=True)
@mock.patch("click.prompt", side_effect=["staging", "fake_api_key"])
@mock.patch("click.confirm", return_value=True)
def test_configure_confirm_yes(mock_confirm, mock_prompt, mock_validate_api_key, mock_get, capsys):
    with fake_creds('.jovian', 'credentials.json'):
        configure()

        assert read_creds() == {'API_KEY': 'fake_api_key',
                                'API_URL': 'https://api-staging.jovian.ai',
                                'GUEST_KEY': ANY,
                                'ORG_ID': 'staging',
                                'WEBAPP_URL': 'https://staging.jovian.ml/'}

        expected_result = """
[jovian] It looks like Jovian is already configured ( check ~/.jovian/credentials.json ).
[jovian] Removing existing configuration..
[jovian] If you're a jovian-pro user please enter your company's organization ID on Jovian (otherwise leave it blank).
[jovian] Please enter your API key ( from https://staging.jovian.ml/ ):
[jovian] Configuration complete!
"""

        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result.strip()


@mock.patch("click.confirm", return_value=False)
def test_configure_confirm_no(mock_confirm, capsys):
    with fake_creds('.jovian', 'credentials.json'):
        configure()

        expected_result = """
[jovian] It looks like Jovian is already configured ( check ~/.jovian/credentials.json ).
[jovian] Skipping..
"""
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result.strip()
