import os
import shutil
from contextlib import contextmanager
from unittest import mock
from unittest.mock import call

import pytest

from jovian.tests.resources import MockResponse, fake_creds
from jovian.utils.clone import _h, clone, get_gist, post_clone_msg, pull


def test_h():
    with fake_creds('.jovian', 'credentials.json'):
        expected_result = {"Authorization": "Bearer fake_api_key",
                           "x-jovian-source": "library",
                           "x-jovian-library-version": "0.2.3",
                           "x-jovian-command": "clone",
                           "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                           "x-jovian-org": "staging"}

        assert _h(True) == expected_result

        expected_result = {"Authorization": "Bearer fake_api_key",
                           "x-jovian-source": "library",
                           "x-jovian-library-version": "0.2.3",
                           "x-jovian-command": "pull",
                           "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                           "x-jovian-org": "staging"}

        assert _h(False) == expected_result


@mock.patch("jovian.utils.clone.get", return_value=MockResponse({'data': {'key': 'value'}}, 200))
def test_get_gist(mock_get):
    with fake_creds('.jovian', 'credentials.json'):
        get_gist('aakashns/jovian-tutorial', 3, fresh=True)

        headers = {"Authorization": "Bearer fake_api_key",
                   "x-jovian-source": "library",
                   "x-jovian-library-version": "0.2.3",
                   "x-jovian-command": "clone",
                   "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                   "x-jovian-org": "staging"}

        mock_get.assert_called_with(
            'https://api-staging.jovian.ai/user/aakashns/gist/jovian-tutorial?gist_version=3', headers=headers)


@mock.patch("jovian.utils.clone.get", return_value=MockResponse({'data': {'key': 'value'}}, 200))
def test_get_gist_only_gist_slug(mock_get):
    with fake_creds('.jovian', 'credentials.json'):
        get_gist('fake_gist_slug', 3, fresh=True)

        headers = {"Authorization": "Bearer fake_api_key",
                   "x-jovian-source": "library",
                   "x-jovian-library-version": "0.2.3",
                   "x-jovian-command": "clone",
                   "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                   "x-jovian-org": "staging"}

        mock_get.assert_called_with(
            'https://api-staging.jovian.ai/gist/fake_gist_slug?gist_version=3', headers=headers)


@mock.patch("jovian.utils.clone.get", return_value=MockResponse({'data': {'key': 'value'}}, 404))
def test_get_gist_raises_exception(mock_get):
    with fake_creds('.jovian', 'credentials.json'):
        with pytest.raises(Exception):
            get_gist('does-not-exist', 3, fresh=True)


def test_post_clone_message(capsys):
    post_clone_msg('jovian-tutorial')

    expected_result = """
[jovian] Cloned successfully to 'jovian-tutorial'

Next steps:
  $ cd jovian-tutorial
  $ jovian install
  $ conda activate <env_name>
  $ jupyter notebook


Replace <env_name> with the name of your environment (without the '<' & '>')
Jovian uses Anaconda ( https://conda.io/ ) under the hood,
so please make sure you have it installed and added to path.
* If you face issues with `jovian install`, try `conda env update`.
* If you face issues with `conda activate`, try `source activate <env_name>`
  or `activate <env_name>` to activate the virtual environment."""

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()


def mock_requests_get(*args, **kwargs):
    ret1 = mock.Mock()
    ret1.content = b""" 
    {
        "cells" : [
            {
                "cell_type": "code",
                "execution_count": 1,
                "metadata": {},
                "outputs": [
                    {
                        "data": {
                            "application/javascript": [
                                "if (window.IPython && IPython.notebook.kernel) IPython.notebook.kernel.execute('jovian.utils.jupyter.get_notebook_name_saved = lambda: \"' + IPython.notebook.notebook_name + '\"')"
                            ],
                            "text/plain": [
                                "<IPython.core.display.Javascript object>"
                            ]
                        },
                        "metadata": {},
                        "output_type": "display_data"
                    }
                ],
                "source": [
                    "import jovian"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }
    """

    ret2 = mock.Mock()
    ret2.content = b"""name: jovian
channels:
  - https://repo.anaconda.com/pkgs/free
  - defaults
dependencies:
  - appdirs=1.4.3
  - appnope=0.1.0
  - asn1crypto=0.24.0
  - attrs=18.2.0
  - automat=0.7.0
  - backcall=0.1.0
  - blas=1.0
  - ca-certifica"""

    return [ret1, ret2] * 3


def mock_get_gist(*args, **kwargs):
    data = {
        "files": [
            {
                "filename": "metrics-example.ipynb",
                "artifact": False,
                "rawUrl": "https://jovian-apiserver-staging.storage.googleapis.com/gists/aakashns/69b13bec3bf04c5b9f01a204940e208f/raw/ae3000d9d061404092f0c9e5ce0fa79c/metrics-example.ipynb",
            },
            {
                "filename": "environment.yml",
                "artifact": False,
                "rawUrl": "https://jovian-apiserver-staging.storage.googleapis.com/gists/aakashns/69b13bec3bf04c5b9f01a204940e208f/raw/08ead271bc8d47b296e282ad375f0ae0/environment.yml",
            },
        ],
        "slug": "69b13bec3bf04c5b9f01a204940e208f",
        "title": "metrics-example",
        "owner": {
            "avatar": "https://api-staging.jovian.ai/api/user/aakashns/avatar",
            "id": 15,
            "name": "aakashns",
            "username": "aakashns"
        }
    }
    return data


@mock.patch("jovian.utils.clone.get", side_effect=mock_requests_get())
@mock.patch("jovian.utils.clone.get_gist", side_effect=mock_get_gist)
def test_clone(mock_get_gist, mock_requests_get):
    try:
        # first time (metric-example)
        clone('aakashns/metrics-example', version='3')
        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', True)

        # second time (metric-example-1)
        os.chdir('..')
        clone('aakashns/metrics-example', version='3')
        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', True)

        # third time (metric-example-2)
        os.chdir('..')
        clone('aakashns/metrics-example', version='3')
        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', True)

    finally:
        # tearDown
        os.chdir('..')
        os.system('rm -rf metrics-example*')


@mock.patch("jovian.utils.clone.get", side_effect=mock_requests_get())
@mock.patch("jovian.utils.clone.get_gist", side_effect=mock_get_gist)
def test_clone_fresh_false(mock_get_gist, mock_requests_get):
    try:
        # first time (metric-example)
        clone('aakashns/metrics-example', version='3')
        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', True)

        # second time (metric-example-1)
        clone('aakashns/metrics-example', version='3', fresh=False)
        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', False)

    finally:
        # tearDown
        os.chdir('..')
        os.system('rm -rf metrics-example*')


@mock.patch("jovian.utils.clone.clone")
def test_pull(mock_clone):
    pull('aakashns/metrics-example', version=3)
    mock_clone.assert_called_with('aakashns/metrics-example', 3, fresh=False)


@mock.patch("jovian.utils.clone.rcfile_exists", return_value=False)
def test_pull_rcfile_does_not_exist(mock_rcfile_exists, capsys):
    pull()

    expected_result = """[jovian] Error: Could not detect '.jovianrc' file. Make sure you are running 'jovian pull' inside a directory cloned with 'jovian clone'."""
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result.strip()


@mock.patch("jovian.utils.clone.rcfile_exists", return_value=False)
def test_pull_rcfile_does_not_exist(mock_rcfile_exists, capsys):
    pull()

    expected_result = """[jovian] Error: Could not detect '.jovianrc' file. Make sure you are running 'jovian pull' inside a directory cloned with 'jovian clone'."""
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result.strip()


@contextmanager
def fake_rcdata():
    data = """{
  "notebooks": {
    "metrics-example.ipynb": {
      "slug": "aakashns/metrics-example"
    },
    "jovian-tutorial.ipynb" : {
      "slug": "aakashns/jovian-tutorial"
    }
  }
}"""
    with open('.jovianrc', 'w') as f:
        f.write(data)

    try:
        yield
    finally:
        os.remove('.jovianrc')


@mock.patch("jovian.utils.clone.clone")
def test_pull_get_latest_notebooks(mock_clone):
    with fake_rcdata():
        pull()

        calls = [
            call('aakashns/metrics-example', None, fresh=False),
            call('aakashns/jovian-tutorial', None, fresh=False),
        ]
        mock_clone.assert_has_calls(calls, any_order=True)
