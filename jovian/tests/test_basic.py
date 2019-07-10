import unittest


class BasicTest(unittest.TestCase):
    def test_string(self):
        a = 'jovian'
        b = 'jovian'
        self.assertEqual(a, b)

    def test_boolean(self):
        a = True
        b = True
        self.assertEqual(a, b)
        self.assertTrue(a)


if __name__ == '__main__':
    unittest.main()
