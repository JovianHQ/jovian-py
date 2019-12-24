import os
from contextlib import contextmanager
from jovian.utils import credentials
from jovian.utils.credentials import config_exists


@contextmanager
def fake_creds(config_dir, creds_filename):
    credentials.CONFIG_DIR = config_dir
    credentials.CREDS_FNAME = creds_filename
    credentials.CREDS_PATH = os.path.join(config_dir, creds_filename)
    yield


def test_config_exits_true():
    with fake_creds('../resources/tmp/', 'credentials.json'):
        assert config_exists() == False
