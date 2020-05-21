import json
import os
import shutil
from contextlib import contextmanager
from unittest import TestCase, mock

import pytest

from jovian.tests.resources.shared import temp_directory
from jovian.utils.constants import RC_FILENAME
from jovian.utils.rcfile import (get_cached_slug, get_notebook_slug, get_rcdata, make_rcdata, rcfile_exists,
                                 reset_notebook_slug, save_rcdata, set_notebook_slug)

_data = {
    "notebooks": {
        "Testing Jovian.ipynb": {
            "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
        }
    }
}


@contextmanager
def fake_rc():
    with temp_directory():
        with open(RC_FILENAME, 'w') as f:
            json.dump(_data, f, indent=2)

        yield


def test_rcfile_does_not_exist():
    with temp_directory():
        assert not rcfile_exists()


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (_data, _data),
        (None, {
            "notebooks": {}
        })
    ]
)
def test_save_rcdata(data, expected_result):
    with temp_directory():
        save_rcdata(data=data)

        with open(RC_FILENAME, 'r') as f:
            assert json.load(f) == expected_result


def test_get_rcdata():
    with temp_directory():
        expected_result = {
            "notebooks": {}
        }
        assert get_rcdata() == expected_result

    with fake_rc():
        assert get_rcdata() == _data


@pytest.mark.parametrize(
    "filename, expected_result",
    [
        ("Testing Jovian.ipynb", "46bd9a3f87e74de0baf8a6f0b60a8df9"),
        ("Testing Jovian123.ipynb", None)
    ]
)
def test_get_notebook_slug_notebook_present(filename, expected_result):
    with fake_rc():
        assert get_notebook_slug(filename) == expected_result


def test_set_notebook_slug():
    with fake_rc():
        filename = "Testing Jovian 2.ipynb"
        slug = "46bd9a3f87e74de0baf8a6f0b60a8df9"

        expected_result = {
            "notebooks": {
                "Testing Jovian.ipynb": {
                    "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
                },
                "Testing Jovian 2.ipynb": {
                    "slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"
                }
            }
        }
        set_notebook_slug(filename, slug)
        assert get_rcdata() == expected_result


def test_make_rcdata():
    filename = "Testing Jovian.ipynb"
    slug = "46bd9a3f87e74de0baf8a6f0b60a8df9"
    expected_result = '{"notebooks": {"Testing Jovian.ipynb": {"slug": "46bd9a3f87e74de0baf8a6f0b60a8df9"}}}'

    assert make_rcdata(filename, slug) == expected_result


@mock.patch("jovian.utils.rcfile._current_slug", "f67108fc906341d8b15209ce88ebc3d2")
def test_get_cached_slug():
    assert get_cached_slug() == "f67108fc906341d8b15209ce88ebc3d2"


@mock.patch("jovian.utils.rcfile._current_slug", "f67108fc906341d8b15209ce88ebc3d2")
def test_reset_notebook_slug():
    assert get_cached_slug() == "f67108fc906341d8b15209ce88ebc3d2"
    reset_notebook_slug()
    assert get_cached_slug() == None
