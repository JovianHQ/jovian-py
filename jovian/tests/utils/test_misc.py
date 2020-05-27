import sys
from unittest import TestCase, mock

import pytest

from jovian._version import __version__
from jovian.utils.constants import LINUX, MACOS, WINDOWS
from jovian.utils.misc import (get_file_extension, get_flavor, get_platform, is_flavor_pro, is_uuid, timestamp_ms,
                               urljoin, version)


@pytest.mark.parametrize(
    "uuid, expected_result",
    [
        ("374ab6086ca449769b3e44b6e35f9126", True),
        ("374ab608-6ca4-4976-9b3e-44b6e35f9126", True),
        ("this-is-not-a-uuid", False),
    ]
)
def test_is_uuid(uuid, expected_result):
    assert is_uuid(uuid) == expected_result


@pytest.mark.parametrize(
    "filename, expected_result",
    [
        ("file.ipynb", ".ipynb"),
        ("file.txt", ".txt"),
        ("file.py", ".py"),
        ("file.csv", ".csv"),
        ("file", ""),
    ]
)
def test_get_file_extension(filename, expected_result):
    assert get_file_extension(filename) == expected_result


@pytest.mark.parametrize(
    "ret_val, expected_result",
    [
        ("Windows", WINDOWS),
        ("Linux", LINUX),
        ("Darwin", MACOS),
    ]
)
def test_get_platform(ret_val, expected_result):
    with mock.patch("platform.system", mock.Mock(return_value=ret_val)):
        assert get_platform() == expected_result


@pytest.mark.parametrize(
    "urls, expected_result",
    [
        (["https://jovian.ml"], "https://jovian.ml"),
        (["https://jovian.ml/"], "https://jovian.ml/"),
        (["///user/siddhant"], "user/siddhant"),
        (["https://jovian.ml", "user/siddhant"], "https://jovian.ml/user/siddhant"),
        (["https://jovian.ml", "/user/siddhant"], "https://jovian.ml/user/siddhant"),
        (["https://jovian.ml/", "user/siddhant"], "https://jovian.ml/user/siddhant"),
        (["https://jovian.ml/", "/user/siddhant"], "https://jovian.ml/user/siddhant"),
        (["https://jovian.ml", "user/siddhant/"], "https://jovian.ml/user/siddhant/"),
        (["https://jovian.ml", "/user/siddhant/"], "https://jovian.ml/user/siddhant/"),
        (["https://jovian.ml/", "user/siddhant/"], "https://jovian.ml/user/siddhant/"),
        (["https://jovian.ml/", "/user/siddhant/"], "https://jovian.ml/user/siddhant/"),
        (["https://jovian.ml/", "///user/siddhant/////"], "https://jovian.ml/user/siddhant/"),
        (["https://jovian.ml/", "user/siddhant/", "/gists/starred"], "https://jovian.ml/user/siddhant/gists/starred"),
    ]
)
def test_urljoin(urls, expected_result):
    assert urljoin(*urls) == expected_result


def test_urljoin_no_args():
    with pytest.raises(TypeError):
        urljoin()


@mock.patch('time.time', mock.Mock(return_value=1577112328.529031))
def test_timestamp_ms():
    assert timestamp_ms() == 1577112328529


def test_get_flavor():
    assert get_flavor() == "jovian"


def test_get_flavor_import_error():
    import builtins
    _original_import = builtins.__import__

    def error_raiser(*args, **kwargs):
        raise ImportError('fake import error')

    builtins.__import__ = error_raiser
    flavor = get_flavor()
    builtins.__import__ = _original_import

    assert flavor == "jovian"


def test_is_flavor_pro_false():
    import jovian._flavor
    jovian._flavor.__flavor__ = 'jovian'
    assert not is_flavor_pro()


def test_is_flavor_pro_true():
    import jovian._flavor
    jovian._flavor.__flavor__ = 'jovian-pro'
    assert is_flavor_pro()


def test_version():
    assert version() == __version__
