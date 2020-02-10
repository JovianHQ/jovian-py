from unittest import TestCase
from jovian.utils.api import _v


class TestV(TestCase):
    def test_v_none(self):
        self.assertEqual(_v(None), '')

    def test_v_number(self):
        self.assertEqual(_v(21), "?gist_version=21")
