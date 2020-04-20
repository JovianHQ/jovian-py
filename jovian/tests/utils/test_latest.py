from textwrap import dedent
from unittest import TestCase, mock

import pytest
from jovian._version import __version__
from jovian.tests.resources.shared import MockResponse
from jovian.utils.latest import _get_latest_version, _print_update_message, check_update
from pkg_resources import parse_version


@mock.patch("requests.get")
def test_get_latest_version_normal(mock_get):
    mock_get().json.return_value = {'info': {'version': '0.2.0.dev1'}}

    expected_result = "0.2.0.dev1"
    assert _get_latest_version() == expected_result


@mock.patch("requests.get", return_value=mock.Mock(return_value=ConnectionError('fake requests.get error')))
def test_get_latest_version_exception(mock_get):
    assert _get_latest_version() == __version__


@pytest.mark.parametrize(
    "in_notebook, expected_result",
    [
        (
            True,
            dedent("""
            [jovian] Update Available: 0.0.1 --> 0.0.2
            [jovian] Run `!pip install jovian --upgrade` to upgrade
            """).strip()
        ),
        (
            False,
            dedent("""
            [jovian] Update Available: 0.0.1 --> 0.0.2
            [jovian] Run `pip install jovian --upgrade` to upgrade
            """).strip()
        ),
    ]
)
def test_print_update_message(in_notebook, expected_result, capsys):
    with mock.patch("jovian.utils.latest.in_notebook", return_value=in_notebook):
        _print_update_message('0.0.1', '0.0.2')
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@pytest.mark.parametrize(
    "probability, expected_result, random_val",
    [
        (1, dedent("""
            [jovian] Update Available: 0.0.1 --> 0.0.2
            [jovian] Run `!pip install jovian --upgrade` to upgrade
            """).strip(), 0.3),
        (None, dedent("""
            [jovian] Update Available: 0.0.1 --> 0.0.2
            [jovian] Run `!pip install jovian --upgrade` to upgrade
            """).strip(), 0.4),
        (None, "", 0.9),
    ]
)
@mock.patch("jovian.utils.latest._get_latest_version", mock.Mock(return_value='0.0.2'))
@mock.patch("jovian.utils.latest.in_notebook", mock.Mock(return_value=True))
def test_check_update(probability, expected_result, random_val, capsys):
    with mock.patch("jovian.utils.latest.random", return_value=random_val):
        import jovian
        jovian.utils.latest.__version__ = '0.0.1'

        if probability:
            check_update(probability)
        else:
            check_update()

        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result
