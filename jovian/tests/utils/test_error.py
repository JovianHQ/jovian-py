from unittest import TestCase
from jovian.utils.error import CondaError, ApiError, ConfigError


class TestCondaError(TestCase):
    def test_conda_error(self):
        msg = 'This is a error'
        e = CondaError(msg)
        self.assertEqual(e.args, (msg,))


class TestApiEror(TestCase):
    def test_api_error(self):
        msg = 'This is a error'
        e = ApiError(msg)
        self.assertEqual(e.args, (msg,))


class TestConfigError(TestCase):
    def test_config_error(self):
        msg = 'This is a error'
        e = ConfigError(msg)
        self.assertEqual(e.args, (msg,))
