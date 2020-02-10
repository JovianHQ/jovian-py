from unittest import TestCase
from jovian._flavor import __flavor__


class TestFlavor(TestCase):
    def test_has_flavor(self):
        self.assertIn(__flavor__, ['jovian', 'jovian-pro'])
