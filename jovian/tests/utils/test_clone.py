import os
import shutil
from contextlib import contextmanager
from unittest import mock
from unittest.mock import call
from textwrap import dedent

import pytest

from jovian.tests.resources.shared import MockResponse, fake_creds, temp_directory
from jovian.utils.clone import _h, clone, get_gist, post_clone_msg, pull
from jovian import __version__

HEADERS = {"Authorization": "Bearer fake_api_key",
           "x-jovian-source": "library",
           "x-jovian-library-version": __version__,
           "x-jovian-command": "clone",
           "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
           "x-jovian-org": "staging"}

FAKE_GIST = {
    "title": "metrics-example",
    "files": [
        {
            "filename": "metrics-example.ipynb",
            "artifact": False,
            "rawUrl": "https://storage.com/slug1"
        },
        {
            "filename": "environment.yml",
            "artifact": False,
            "rawUrl": "https://storage.com/slug2"
        },
    ],
}


@pytest.mark.parametrize(
    "command, fresh",
    [
        ("clone", True),
        ("pull", False),
    ]
)
def test_h(command, fresh):
    with fake_creds():
        expected_result = {"Authorization": "Bearer fake_api_key",
                           "x-jovian-source": "library",
                           "x-jovian-library-version": __version__,
                           "x-jovian-command": command,
                           "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                           "x-jovian-org": "staging"}

        assert _h(fresh=fresh) == expected_result


@pytest.mark.parametrize(
    "gist, called_with_url",
    [
        (
            'aakashns/jovian-tutorial',
            'https://api-staging.jovian.ai/user/aakashns/gist/jovian-tutorial?gist_version=3',
        ),
        (
            'fake_gist_slug',
            'https://api-staging.jovian.ai/gist/fake_gist_slug?gist_version=3',
        ),
    ]
)
@mock.patch("jovian.utils.clone.get", return_value=MockResponse({'data': {'key': 'value'}}, 200))
def test_get_gist(mock_get, gist, called_with_url):
    with fake_creds():
        get_gist(gist, 3, fresh=True)

        mock_get.assert_called_with(called_with_url, headers=HEADERS)


@mock.patch("jovian.utils.clone.get", return_value=MockResponse({'data': {'key': 'value'}}, 404))
def test_get_gist_raises_exception(mock_get):
    with fake_creds():
        with pytest.raises(Exception):
            get_gist('does-not-exist', 3, fresh=True)


def test_post_clone_message(capsys):
    post_clone_msg('jovian-tutorial')

    expected_result = dedent("""
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
              or `activate <env_name>` to activate the virtual environment.""").strip()

    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()


@mock.patch("jovian.utils.clone.get")
@mock.patch("jovian.utils.clone.get_gist")
def test_clone(mock_get_gist, mock_requests_get):
    with temp_directory() as dir:
        mock_get_gist.return_value = FAKE_GIST

        get1, get2 = mock.Mock(), mock.Mock()
        get1.content, get2.content = b"notebook content", b"environment content"

        mock_requests_get.side_effect = [get1, get2]

        clone('aakashns/metrics-example', version='3')

        os.chdir(dir)

        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', True)
        mock_requests_get.assert_has_calls([
            call("https://storage.com/slug1"),
            call("https://storage.com/slug2")
        ])

        # Check that folder was created
        assert os.listdir() == ["metrics-example"]

        # Check that files were downloaded
        assert set(os.listdir("metrics-example")) == {".jovianrc", "environment.yml", "metrics-example.ipynb"}


@mock.patch("jovian.utils.clone.get")
@mock.patch("jovian.utils.clone.get_gist")
def test_clone_multiple(mock_get_gist, mock_requests_get):
    with temp_directory() as dir:
        mock_get_gist.return_value = FAKE_GIST

        get1, get2 = mock.Mock(), mock.Mock()
        get1.content, get2.content = b"notebook content", b"environment content"

        mock_requests_get.side_effect = [get1, get2] * 3

        # first call
        clone('aakashns/metrics-example', version='3')
        os.chdir(dir)

        # second call
        clone('aakashns/metrics-example', version='3')
        os.chdir(dir)

        # third call
        clone('aakashns/metrics-example', version='3')
        os.chdir(dir)

        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', True)
        mock_requests_get.assert_has_calls([
            call("https://storage.com/slug1"),
            call("https://storage.com/slug2")
        ] * 3)

        # Check that multiple folders were created
        assert set(os.listdir()) == {"metrics-example", "metrics-example-1", "metrics-example-2"}


@mock.patch("jovian.utils.clone.get")
@mock.patch("jovian.utils.clone.get_gist")
def test_clone_fresh_false(mock_get_gist, mock_requests_get):
    with temp_directory() as dir:
        mock_get_gist.return_value = FAKE_GIST

        get1, get2 = mock.Mock(), mock.Mock()
        get1.content, get2.content = b"notebook content", b"environment content"

        mock_requests_get.side_effect = [get1, get2]

        clone('aakashns/metrics-example', version='3', fresh=False)

        os.chdir(dir)

        mock_get_gist.assert_called_with('aakashns/metrics-example', '3', False)
        mock_requests_get.assert_has_calls([
            call("https://storage.com/slug1"),
            call("https://storage.com/slug2")
        ])

        # Check that directory was not created
        assert "metrics-example" not in os.listdir()

        # Check that files were downloaded
        assert set(os.listdir()) == {"environment.yml", "metrics-example.ipynb"}


@mock.patch("jovian.utils.clone.get")
@mock.patch("jovian.utils.clone.get_gist")
def test_clone_overwrite(mock_get_gist, mock_requests_get):
    with temp_directory() as dir:
        mock_get_gist.return_value = FAKE_GIST

        get1, get2 = mock.Mock(), mock.Mock()
        get1.content, get2.content = b"notebook content", b"environment content"

        mock_requests_get.side_effect = [get1, get2] * 2

        clone('aakashns/metrics-example', version='3')
        os.chdir(dir)

        # Check that directory was created
        assert "metrics-example" in os.listdir()

        clone('aakashns/metrics-example', version='3', overwrite=True)
        os.chdir(dir)

        # Check that another directory was not created
        assert os.listdir() == ["metrics-example"]


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


@contextmanager
def fake_rcdata():
    with temp_directory():
        data = dedent("""
                {
                    "notebooks": {
                        "metrics-example.ipynb": {
                        "slug": "aakashns/metrics-example"
                        },
                        "jovian-tutorial.ipynb" : {
                        "slug": "aakashns/jovian-tutorial"
                        }
                    }
                }""").strip()

        with open('.jovianrc', 'w') as f:
            f.write(data)

        yield


@mock.patch("jovian.utils.clone.clone")
def test_pull_get_latest_notebooks(mock_clone):
    with fake_rcdata():
        pull()

        calls = [
            call('aakashns/metrics-example', None, fresh=False),
            call('aakashns/jovian-tutorial', None, fresh=False),
        ]
        mock_clone.assert_has_calls(calls, any_order=True)
