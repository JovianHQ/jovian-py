from unittest import TestCase, mock
from jovian.utils.script import get_script_filename, in_script


class TestGetScriptFilename(TestCase):

    def test_get_script_filename_normal(self):
        import __main__
        __main__.__file__ = 'sample.py'

        expected_result = 'sample.py'
        self.assertEqual(get_script_filename(), expected_result)

    @mock.patch('builtins.__import__', return_value=ImportError('fake import error'))
    def test_get_script_filename_exception(self, mock_import):

        expected_result = None
        self.assertEqual(get_script_filename(), expected_result)


class TestInScript(TestCase):

    def test_in_script_valid_extension(self):
        import __main__
        __main__.__file__ = 'sample.py'

        self.assertTrue(in_script())

    def test_in_script_invalid_extension(self):
        import __main__
        __main__.__file__ = 'sample.txt'

        self.assertFalse(in_script())

    def test_in_script_false(self):
        import __main__
        __main__.__file__ = None

        self.assertFalse(in_script())
