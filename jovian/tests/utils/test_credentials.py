import os
from contextlib import contextmanager
from jovian.utils import credentials
from jovian.utils.credentials import config_exists, purge_config


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

# def test_read_creds_valid():
#     with fake_creds('.jovian-purge', 'credentials.json'):
