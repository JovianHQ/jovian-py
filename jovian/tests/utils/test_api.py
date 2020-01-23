from unittest import TestCase, mock
from contextlib import contextmanager
from jovian.utils import credentials
from jovian.utils.credentials import write_creds, purge_config
from jovian.utils.api import _v, _h, _u, get_current_user, get_gist, get_gist_access


@contextmanager
def fake_creds(config_dir, creds_filename, purge=False):
    _d, _f = credentials.CONFIG_DIR, credentials.CREDS_FNAME
    credentials.CONFIG_DIR = 'jovian/tests/resources/creds/' + config_dir
    credentials.CREDS_FNAME = creds_filename
    try:
        yield
    finally:
        if purge:
            purge_config()
    credentials.CONFIG_DIR = _d
    credentials.CREDS_FNAME = _f


class MockResponse:
    def __init__(self, json_data, status_code, text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data


def mock_requests_get(url, *args, **kwargs):
    if url == 'https://api-staging.jovian.ai/user/profile':
        if kwargs['headers']['Authorization'] == 'Bearer fake_api_key':
            data = {
                "data": {
                    "id": 47,
                    "username": "rohit"
                },
                "success": True
            }

            return MockResponse(data, status_code=200)
        else:
            data = {
                "errors": [
                    {
                        "code": 401,
                        "message": "Signature verification failed"
                    }
                ],
                "success": False
            }
            return MockResponse(data, status_code=401)
    elif url == 'https://api-staging.jovian.ai/user/rohit/gist/demo-notebook' or \
        url == 'https://api-staging.jovian.ai/user/rohit/gist/demo-notebook?gist_version=3' or \
        url == 'https://api-staging.jovian.ai/gist/f67108fc906341d8b15209ce88ebc3d2':

            data = {
                "data": {
                    "archived": False,
                    "clonesCount": 0,
                    "createdAt": 1578718557994,
                    "currentUser": {
                        "id": 47,
                        "username": "rohit"
                    },
                    "deleted": False,
                    "description": None
                }
            }

            return MockResponse(data, status_code=200)

    elif url == 'https://api-staging.jovian.ai/gist/fake_nonexistent_gist':
        data = {
            "errors": [
                {
                    "code": 404,
                    "message": "Gist not found"
                }
            ],
            "success": False
        }
        return MockResponse(data, status_code=404)

    elif url == 'https://api-staging.jovian.ai/gist/fake_gist_too_large':
        return MockResponse({'message' : 'Internal Server Error'}, status_code=500)

    elif url == 'https://api-staging.jovian.ai/gist/f67108fc906341d8b15209ce88ebc3d2/check-access':
            data = {
                "data": {
                    "currentUser": {
                        "id": 47,
                        "username": "rohit"
                    },
                    "read": True,
                    "slug": "f67108fc906341d8b15209ce88ebc3d2",
                    "write": True
                },
                "success": True
            }
            return MockResponse(data, status_code=200)
    elif url == 'https://api-staging.jovian.ai/gist/fake_nonexistent_gist/check-access':
        data = {
            "errors": [
                {
                    "code": 404,
                    "message": "Gist not found"
                }
            ],
            "success": False
        }
        return MockResponse(data, status_code=404)


class TestV(TestCase):
    def test_v_none(self):
        self.assertEqual(_v(None), '')

    def test_v_number(self):
        self.assertEqual(_v(21), "?gist_version=21")


def test_h():
    with fake_creds('.jovian', 'credentials.json'):
        expected_result = {"Authorization": "Bearer fake_api_key",
                           "x-jovian-source": "library",
                           "x-jovian-library-version": "0.2.3",
                           "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                           "x-jovian-org": "staging"}

        assert _h() == expected_result


def test_u():
    with fake_creds('.jovian', 'credentials.json'):
        path = 'user/profile'

        assert _u(path) == 'https://api-staging.jovian.ai/user/profile'


class TestGetCurrentUser(TestCase):
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_current_user(self, mock_requests_get):
        with fake_creds('.jovian', 'credentials.json'):
            expected_result = {
                "id": 47,
                "username": "rohit"
            }

            assert get_current_user() == expected_result

    @mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_current_user_raises_exception(self, mock_requests_get, mock_get_api_key):
        with fake_creds('.jovian-invalid-key', 'credentials.json', purge=True):
            # setUp
            creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                     "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                     "API_URL": "https://api-staging.jovian.ai",
                     "API_KEY": "fake_invalid_api_key",
                     "ORG_ID": "staging"}
            write_creds(creds)

            with self.assertRaises(Exception) as context:
                get_current_user()

            assert context.exception.args[0] == 'Failed to fetch current user profile. (HTTP 401) Signature verification failed'

class TestGetGist(TestCase):
    @mock.patch("jovian.utils.api.get_api_key", return_value="fake_api_key")
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_gist(self, mock_requests_get, mock_get_api_key):
        with fake_creds('.jovian', 'credentials.json'):
            expected_result = {
                "archived": False,
                "clonesCount": 0,
                "createdAt": 1578718557994,
                "currentUser": {
                    "id": 47,
                    "username": "rohit"
                },
                "deleted": False,
                "description": None
            }

            assert get_gist('rohit/demo-notebook') == expected_result

            assert get_gist('rohit/demo-notebook', version=3) == expected_result

            assert get_gist('f67108fc906341d8b15209ce88ebc3d2') == expected_result


    @mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_gist_not_found(self, mock_requests_get, mock_get_api_key):
        with fake_creds('.jovian', 'credentials.json'):
            assert get_gist('fake_nonexistent_gist') == False

    @mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_gist_raises_exception(self, mock_requests_get, mock_get_api_key):
        with fake_creds('.jovian', 'credentials.json'):
            assert get_gist('fake_nonexistent_gist') == False

    @mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_gist_raises_exception(self, mock_requests_get, mock_get_api_key):
        with fake_creds('.jovian', 'credentials.json'):
            with self.assertRaises(Exception) as context:
                get_gist('fake_gist_too_large')

            assert context.exception.args[0] == 'Failed to retrieve metadata for notebook "fake_gist_too_large":'+ \
                                                ' (HTTP 500) Internal Server Error'

class TestGetGistAccess(TestCase):
    
    @mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_gist_access(self, mock_requests_get, mock_get_api_key):
        with fake_creds('.jovian', 'credentials.json'):
            expected_result = {
                "currentUser": {
                    "id": 47,
                    "username": "rohit"
                },
                "read": True,
                "slug": "f67108fc906341d8b15209ce88ebc3d2",
                "write": True
            }
            assert get_gist_access('f67108fc906341d8b15209ce88ebc3d2') == expected_result
    
    @mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
    @mock.patch("requests.get", side_effect=mock_requests_get)
    def test_get_gist_access_raises_exception(self, mock_requests_get, mock_get_api_key):
        with fake_creds('.jovian', 'credentials.json'):
            with self.assertRaises(Exception) as context:
                get_gist_access('fake_nonexistent_gist')
            
            assert context.exception.args[0] == 'Failed to retrieve access permission for notebook' + \
                ' "fake_nonexistent_gist" (retry with create_new=True to create a new notebook):' +\
                ' (HTTP 404) Gist not found'