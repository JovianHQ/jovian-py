import os
from contextlib import contextmanager
from jovian.utils import credentials
from jovian.utils.credentials import (get_creds_path, config_exists, purge_config, init_config, purge_creds, read_creds,
                                      creds_exist, read_cred, write_creds, purge_cred_key, write_cred)


@contextmanager
def fake_creds(config_dir, creds_filename):
    _d, _f = credentials.CONFIG_DIR, credentials.CREDS_FNAME
    credentials.CONFIG_DIR = 'jovian/tests/resources/creds/' + config_dir
    credentials.CREDS_FNAME = creds_filename
    yield
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
    with fake_creds('.jovian-init-config', 'credentials.json'):
        init_config()
        assert os.path.exists('jovian/tests/resources/creds/.jovian-init-config') == True
        purge_config()


def test_purge_creds():
    with fake_creds('.jovian-purge-creds', 'credentials.json'):
        os.makedirs(credentials.CONFIG_DIR, exist_ok=True)
        os.system('touch jovian/tests/resources/creds/.jovian-purge-creds/credentials.json')
        assert os.path.exists('jovian/tests/resources/creds/.jovian-purge-creds/credentials.json') == True
        purge_creds()
        assert os.path.exists('jovian/tests/resources/creds/.jovian-purge-creds/credentials.json') == False
        purge_config()


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
    with fake_creds('.jovian-write-creds', 'credentials.json'):
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        assert read_creds() == creds

        purge_config()


def test_write_cred():
    with fake_creds('.jovian-write-cred', 'credentials.json'):
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

        purge_config()


def test_write_cred_already_exists():
    with fake_creds('.jovian-write-cred', 'credentials.json'):
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        write_cred('ORG_ID', 'staging')

        expected_result = creds
        assert read_creds() == expected_result

        purge_config()


def test_purge_cred_key():
    with fake_creds('.jovian-write-creds', 'credentials.json'):
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

        purge_config()
