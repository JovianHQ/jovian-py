from unittest import mock
import pytest
from jovian.utils.clone import _h, get_gist, post_clone_msg, clone, pull
from jovian.tests.resources import fake_creds, MockResponse


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
