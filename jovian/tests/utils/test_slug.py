from jovian.utils.slug import get_current_slug, set_current_slug
from jovian.utils import slug
from unittest import mock


@mock.patch("jovian.utils.slug._current_slug", "test_slug")
def test_get_current_slug():
    assert get_current_slug() == "test_slug"


@mock.patch("jovian.utils.slug.get_notebook_slug", return_value="test_slug")
def test_set_current_slug(mock_get_notebook_slug):
    set_current_slug("fake_filename")
    assert slug._current_slug == "test_slug"
