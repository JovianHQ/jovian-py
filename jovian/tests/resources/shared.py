import os
import textwrap
from contextlib import contextmanager
from subprocess import check_call
from tempfile import TemporaryDirectory
from textwrap import dedent

from jovian.utils import credentials
from jovian.utils.credentials import purge_config, write_creds


@contextmanager
def fake_creds(config_dir='.jovian', creds_filename='credentials.json', extra=None):
    with temp_directory() as dir:
        _d, _f = credentials.CONFIG_DIR, credentials.CREDS_FNAME
        credentials.CONFIG_DIR = os.path.join(dir, config_dir)
        credentials.CREDS_FNAME = creds_filename
        creds = {
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "WEBAPP_URL": "https://staging.jovian.ai/",
            "ORG_ID": "staging",
            "API_KEY": "fake_api_key",
        }

        if extra and isinstance(extra, dict):
            creds.update(extra)

        write_creds(creds)
        try:
            yield dir
        finally:
            purge_config()
        credentials.CONFIG_DIR = _d
        credentials.CREDS_FNAME = _f


@contextmanager
def temp_directory():
    orig_path = os.getcwd()
    try:
        with TemporaryDirectory() as dir:
            os.chdir(dir)
            yield dir
    finally:
        os.chdir(orig_path)


@contextmanager
def mock_git_repo():
    orig_dir = os.getcwd()
    with temp_directory() as dir:
        os.mkdir("mock_git_repo")
        os.chdir("mock_git_repo")

        commands = textwrap.dedent("""
        git init
        git remote add origin https://github.com/JovianML/mock_repo.git
        touch notebook.ipynb
        git add .
        git commit -m "initialcommit"
        """).splitlines()[1:]

        for command in commands:
            check_call(command.split())

        yield dir
    os.chdir(orig_dir)


@contextmanager
def fake_records():
    import jovian.utils.records
    _d = jovian.utils.records._data_blocks
    jovian.utils.records._data_blocks = [('fake_slug_metrics_1', 'metrics', {}),
                                         ('fake_slug_metrics_2', 'metrics', {}),
                                         ('fake_slug_hyperparams_1', 'hyperparams', {}),
                                         ('fake_slug_hyperparams_2', 'hyperparams', {})]

    try:
        yield
    finally:
        jovian.utils.records._data_blocks = _d


@contextmanager
def fake_envfile(fname='environment.yml'):
    with temp_directory():
        with open('empty-yaml-file.yml', 'w') as f:
            f.write("")

        with open(fname, 'w') as f:
            data = dedent("""
            channels:
                - defaults
            dependencies:
                - mixpanel=1.11.0
                - sigmasix=1.91.0
                - sqlite
                - pip:
                    - six==1.11.0
                    - sqlite==2.0.0
            name: test-env
            prefix: /home/admin/anaconda3/envs/test-env
            """)
            f.write(data)
        yield


def touch(file):
    """Create an empty file with touch"""
    os.system("touch {}".format(file))


class MockResponse:
    def __init__(self, json_data, status_code, text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data
