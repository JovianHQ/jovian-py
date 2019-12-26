from unittest import TestCase
from jovian._version import __version__


class TestVersion(TestCase):
    def test_version(self):
        self.assertIsInstance(__version__, str)
