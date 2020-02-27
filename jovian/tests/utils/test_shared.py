from jovian.tests.resources import fake_creds
from jovian.utils.shared import _u, _v


def test_v():
    assert _v(3) == "?gist_version=3"
    assert _v(None) == ""


def test_u():
    with fake_creds('.jovian', 'credentials.json'):
        path = 'user/profile'

        assert _u(path) == 'https://api-staging.jovian.ai/user/profile'
