from unittest import TestCase, mock
from jovian.utils.script import get_script_filename, in_script


def test_get_script_filename_normal():
    import __main__
    __main__.__file__ = 'sample.py'

    expected_result = 'sample.py'
    assert get_script_filename() == expected_result


@mock.patch('builtins.__import__', return_value=ImportError('fake import error'))
def test_get_script_filename_exception(mock_import):

    expected_result = None
    assert get_script_filename() == expected_result


def test_in_script_valid_extension():
    import __main__
    __main__.__file__ = 'sample.py'

    assert in_script()


def test_in_script_invalid_extension():
    import __main__
    __main__.__file__ = 'sample.txt'

    assert in_script()


def test_in_script_false():
    import __main__
    __main__.__file__ = None

    assert not in_script()
