from unittest import TestCase, mock
from jovian._version import __version__
from pkg_resources import parse_version

from jovian.utils.latest import _get_latest_version, _print_update_message, check_update


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


@mock.patch("requests.get", mock.Mock(return_value=MockResponse({'info': {'version': '0.2.0.dev1'}}, 200)))
def test_get_latest_version_normal():
    expected_result = "0.2.0.dev1"
    assert _get_latest_version() == expected_result


@mock.patch("requests.get", mock.Mock(return_value=ConnectionError('fake requests.get error')))
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
def test_check_update(capsys):
    expected_result = """[jovian] Update Available: 0.0.1 --> 0.0.2
[jovian] Run `pip install jovian --upgrade` to upgrade"""

    import jovian
    jovian.utils.latest.__version__ = '0.0.1'

    check_update(1)
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.latest._get_latest_version", mock.Mock(return_value='0.0.2'))
@mock.patch("jovian.utils.latest.random", mock.Mock(return_value=0.5))
def test_check_update_mock_random(capsys):
    expected_result = """[jovian] Update Available: 0.0.1 --> 0.0.2
[jovian] Run `pip install jovian --upgrade` to upgrade"""

    import jovian
    jovian.utils.latest.__version__ = '0.0.1'

    check_update()
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.latest._get_latest_version", mock.Mock(return_value='0.0.2'))
@mock.patch("jovian.utils.latest.random", mock.Mock(return_value=0.9))
def test_check_update_mock_random_no_output(capsys):
    expected_result = ""

    import jovian
    jovian.utils.latest.__version__ = '0.0.1'

    check_update()
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result
