from unittest import TestCase, mock
from jovian._version import __version__
from pkg_resources import parse_version

from jovian.utils.latest import _get_latest_version, _print_update_message, check_update


@mock.patch("jovian.utils.latest.requests.get", mock.Mock(return_value="0.2.0"))
def test_get_latest_version_normal():
    expected_result = __version__
    assert _get_latest_version() == expected_result


@mock.patch("jovian.utils.latest.requests.get", mock.Mock(return_value=ConnectionError('fake requests.get error')))
def test_get_latest_version_exception():
    expected_result = __version__
    assert _get_latest_version() == expected_result


@mock.patch("jovian.utils.latest.in_notebook", mock.Mock(return_value=True))
def test_print_update_message_in_notebook(capsys):
    expected_result = """[jovian] Update Available: 0.0.1 --> 0.0.2
[jovian] Run `!pip install jovian --upgrade` to upgrade"""

    _print_update_message('0.0.1', '0.0.2')
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.latest.in_notebook", mock.Mock(return_value=False))
def test_print_update_message_not_in_notebook(capsys):
    expected_result = """[jovian] Update Available: 0.0.1 --> 0.0.2
[jovian] Run `pip install jovian --upgrade` to upgrade"""

    _print_update_message('0.0.1', '0.0.2')
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.latest._get_latest_version", mock.Mock(return_value='0.0.2'))
def test_get_update(capsys):
    expected_result = """[jovian] Update Available: 0.0.1 --> 0.0.2
[jovian] Run `pip install jovian --upgrade` to upgrade"""

    import jovian
    jovian.utils.latest.__version__ = '0.0.1'

    check_update(1)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result
