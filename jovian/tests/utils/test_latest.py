from unittest import TestCase, mock
from jovian._version import __version__
from pkg_resources import parse_version

from jovian.utils.latest import _get_latest_version, _print_update_message, check_update


class TestGetLatestVersion(TestCase):
    def error_raiser(*args, **kwargs):
        raise ImportError('fake requests.get error')

    @mock.patch("jovian.utils.latest.requests.get", mock.Mock(return_value=error_raiser))
    def test_get_latest_version_exception(self):
        expected_result = __version__
        self.assertEqual(_get_latest_version(), expected_result)


class TestPrintUpdateMessage(TestCase):

    @mock.patch("jovian.utils.latest.log")
    def test_print_update_message_normal(self, mock_log):
        current_version = '0.0.1'
        latest_version = '0.0.2'
        expected_result = 'Update Available: {0} --> {1}'.format(current_version, latest_version)
        _print_update_message(current_version, latest_version)
        mock_log.assert_any_call(expected_result)

    @mock.patch("jovian.utils.latest.in_notebook", mock.Mock(return_value=True))
    @mock.patch("jovian.utils.latest.log")
    def test_print_update_message_in_notebook(self, mock_log):
        current_version = '0.0.1'
        latest_version = '0.0.2'
        expected_result = 'Run `!pip install jovian --upgrade` to upgrade'
        _print_update_message(current_version, latest_version)
        mock_log.assert_any_call(expected_result)

    @mock.patch("jovian.utils.latest.in_notebook", mock.Mock(return_value=False))
    @mock.patch("jovian.utils.latest.log")
    def test_print_update_message_not_in_notebook(self, mock_log):
        current_version = '0.0.1'
        latest_version = '0.0.2'
        expected_result = 'Run `pip install jovian --upgrade` to upgrade\n'
        _print_update_message(current_version, latest_version)
        mock_log.assert_any_call(expected_result)


class TestGetUpdate(TestCase):
    current_version = '0.0.1'
    latest_version = '0.0.2'
    @mock.patch("jovian.utils.latest._get_latest_version", mock.Mock(return_value=latest_version))
    @mock.patch("jovian.utils.latest._print_update_message")
    def test_get_update(self, mock_print_update_message):
        import jovian
        jovian.utils.latest.__version__ = '0.0.1'
        check_update(1)
        mock_print_update_message.assert_called_with(
            parse_version(self.current_version),
            parse_version(self.latest_version))
