from unittest import TestCase
from jovian._version import __version__


def test_version():
    assert isinstance(__version__, str)
