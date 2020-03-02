from contextlib import contextmanager
from jovian.utils import credentials
from jovian.utils.credentials import write_creds, purge_config


@contextmanager
def fake_creds(config_dir='.jovian', creds_filename='credentials.json'):
    _d, _f = credentials.CONFIG_DIR, credentials.CREDS_FNAME
    credentials.CONFIG_DIR = 'jovian/tests/resources/creds/' + config_dir
    credentials.CREDS_FNAME = creds_filename
    creds = {
        "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
        "API_URL": "https://api-staging.jovian.ai",
        "WEBAPP_URL": "https://staging.jovian.ml/",
        "ORG_ID": "staging",
        "API_KEY": "fake_api_key"
    }
    write_creds(creds)
    try:
        yield
    finally:
        purge_config()
    credentials.CONFIG_DIR = _d
    credentials.CREDS_FNAME = _f


class MockResponse:
    def __init__(self, json_data, status_code, text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data
