from unittest import TestCase, mock
import pytest
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


@pytest.mark.parametrize(
    "filename, expected_result",
    [
        ('sample.py', True),
        ('sample.txt', False),
        (None, False)
    ]
)
def test_in_script(filename, expected_result):
    import __main__
    __main__.__file__ = filename

    assert in_script() == expected_result
