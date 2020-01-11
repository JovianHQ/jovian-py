import os
from unittest import mock
from contextlib import contextmanager
from jovian.utils import credentials
from jovian.utils.credentials import (get_creds_path, config_exists, purge_config, init_config, purge_creds, read_creds,
                                      creds_exist, read_cred, write_creds, purge_cred_key, write_cred, write_api_url,
                                      request_org_id, write_org_id, read_api_url, read_org_id, write_webapp_url, 
                                      read_webapp_url, ensure_org)


@contextmanager
def fake_creds(config_dir, creds_filename, purge=False):
    _d, _f = credentials.CONFIG_DIR, credentials.CREDS_FNAME
    credentials.CONFIG_DIR = 'jovian/tests/resources/creds/' + config_dir
    credentials.CREDS_FNAME = creds_filename
    try:
        yield
    finally:
        if purge:
            purge_config()
    credentials.CONFIG_DIR = _d
    credentials.CREDS_FNAME = _f


def test_config_exits_false():
    with fake_creds('.jovian-does-not-exist', 'credentials.json'):
        assert config_exists() == False


def test_config_exists_true():
    with fake_creds('.jovian', 'credentials.json'):
        print(credentials.CONFIG_DIR)
        print(os.path.exists(credentials.CONFIG_DIR))
        assert config_exists() == True


def test_purge_config():
    with fake_creds('.jovian-purge', 'credentials.json'):
        os.makedirs(credentials.CONFIG_DIR, exist_ok=True)
        assert config_exists() == True
        purge_config()
        assert config_exists() == False


def test_get_creds_path():
    with fake_creds('.jovian', 'credentials.json'):
        assert get_creds_path() == 'jovian/tests/resources/creds/.jovian/credentials.json'


def test_init_config():
    with fake_creds('.jovian-init-config', 'credentials.json', purge=True):
        init_config()
        assert os.path.exists('jovian/tests/resources/creds/.jovian-init-config') == True


def test_purge_creds():
    with fake_creds('.jovian-purge-creds', 'credentials.json', purge=True):
        os.makedirs(credentials.CONFIG_DIR, exist_ok=True)
        os.system('touch jovian/tests/resources/creds/.jovian-purge-creds/credentials.json')
        assert os.path.exists('jovian/tests/resources/creds/.jovian-purge-creds/credentials.json') == True
        purge_creds()
        assert os.path.exists('jovian/tests/resources/creds/.jovian-purge-creds/credentials.json') == False


def test_read_creds_no_creds_folder():
    with fake_creds('.jovian-no-creds', 'credentials.json'):
        assert read_creds() == {}


def test_read_creds_folder_exists():
    with fake_creds('.jovian', 'credentials.json'):
        expected_result = {"WEBAPP_URL": "https://staging.jovian.ml/",
                           "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                           "ORG_ID": "staging",
                           "API_URL": "https://api-staging.jovian.ai",
                           "API_KEY": "fake_api_key"}
        assert read_creds() == expected_result


def mock_json_load(*args, **kwargs):
    raise ValueError('fake value error')


@mock.patch("jovian.utils.credentials.purge_creds", return_value=None)
@mock.patch("json.load", side_effect=mock_json_load)
def test_read_creds_with_value_error(mock_json_load, mock_purge_creds):
    with fake_creds('.jovian', 'credentials.json'):
        assert read_creds() == {}


def test_creds_exist_true():
    with fake_creds('.jovian', 'credentials.json'):
        assert creds_exist() == True


def test_creds_exist_false():
    with fake_creds('.jovian', 'credentials-no-api-key.json'):
        assert creds_exist() == False


def test_read_cred_no_default():
    with fake_creds('.jovian', 'credentials.json'):
        assert read_cred('ORG_ID') == 'staging'


def test_read_cred_with_default():
    with fake_creds('.jovian', 'credentials.json'):
        assert read_cred('FAKE_ID', 'default_value') == 'default_value'


def test_write_creds():
    with fake_creds('.jovian-write-creds', 'credentials.json', purge=True):
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        assert read_creds() == creds


def test_write_cred():
    with fake_creds('.jovian-write-cred', 'credentials.json', purge=True):
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        write_cred('FAKE_KEY', 'fake_value')

        expected_result = {"WEBAPP_URL": "https://staging.jovian.ml/",
                           "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                           "ORG_ID": "staging",
                           "API_URL": "https://api-staging.jovian.ai",
                           "FAKE_KEY": "fake_value"}
        assert read_creds() == expected_result


def test_write_cred_already_exists():
    with fake_creds('.jovian-write-cred', 'credentials.json', purge=True):
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        write_cred('ORG_ID', 'staging')

        expected_result = creds
        assert read_creds() == expected_result


def test_purge_cred_key():
    with fake_creds('.jovian-write-creds', 'credentials.json', purge=True):
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        purge_cred_key('GUEST_KEY')

        expected_result = {"WEBAPP_URL": "https://staging.jovian.ml/",
                           "ORG_ID": "staging",
                           "API_URL": "https://api-staging.jovian.ai"}

        assert read_creds() == expected_result


def test_write_api_url():
    with fake_creds('.jovian-write-api-url', 'credentials.json', purge=True):
        write_api_url("https://fake_api.jovian.ai/")

        from jovian.utils.credentials import API_URL_KEY
        assert read_cred(API_URL_KEY) == "https://fake_api.jovian.ai/"

def test_read_api_url():
    with fake_creds('.jovian-write-api-url', 'credentials.json', purge=True):
        write_api_url("https://fake_api.jovian.ai/")
        assert read_api_url() == "https://fake_api.jovian.ai/"

def test_write_org_id():
    with fake_creds('.jovian-write-api-url', 'credentials.json', purge=True):
        write_org_id("fake_org_id")

        from jovian.utils.credentials import ORG_ID_KEY
        assert read_cred(ORG_ID_KEY) == "fake_org_id"


def test_read_org_id():
    with fake_creds('.jovian-write-api-url', 'credentials.json', purge=True):
        write_org_id("fake_org_id")
        assert read_org_id() == "fake_org_id"

def test_write_webapp_url():
    with fake_creds('.jovian-write-api-url', 'credentials.json', purge=True):
        write_webapp_url("http://fake-webapp-url.ai/")

        from jovian.utils.credentials import WEBAPP_URL_KEY
        assert read_cred(WEBAPP_URL_KEY) == "http://fake-webapp-url.ai/"


def test_read_webapp_url():
    with fake_creds('.jovian-write-api-url', 'credentials.json', purge=True):
        write_webapp_url("http://fake-webapp-url.ai/")
        assert read_webapp_url() == "http://fake-webapp-url.ai/"


@mock.patch("click.prompt", return_value="fake_org_id")
def test_request_org_id(mock_prompt):
    assert request_org_id() == "fake_org_id"

@mock.patch("jovian.utils.credentials.is_flavor_pro", return_value=True)
def test_ensure_org_all_creds_exist(mock_is_flavor_pro):
    with fake_creds('.jovian', 'credentials.json'):
        assert ensure_org() == None
