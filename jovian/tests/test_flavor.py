from unittest import TestCase
from jovian._flavor import __flavor__


def test_has_flavor():
    assert __flavor__ in ['jovian', 'jovian-pro']
