from unittest import TestCase, mock

from jovian.tests.resources import fake_creds
from jovian.utils.configure import configure, reset_config
from jovian.utils.credentials import creds_exist, purge_creds


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
