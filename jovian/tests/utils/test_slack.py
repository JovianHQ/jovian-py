import os
from contextlib import contextmanager
from unittest import TestCase, mock
from jovian.utils import slack
from jovian.utils import credentials
from jovian.utils.credentials import write_creds, purge_config
from jovian.utils.slack import _u, _h, _v, add_slack, notify
from jovian.utils.error import ApiError

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

def test_u():
    with fake_creds('.jovian', 'credentials.json'):
        path = 'user/profile'

        assert _u(path) == 'https://api-staging.jovian.ai/user/profile'

def test_h():
    with fake_creds('.jovian', 'credentials.json'):
        expected_result = {"Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": "0.2.0.dev1",
                "x-jovian-command": "add-slack",
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging"}
        
        assert _h() == expected_result

def test_v():
    assert _v(3) == "?gist_version=3"
    assert _v(None) == ""

class MockResponse:
    def __init__(self, json_data, status_code, text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text
    def json(self):
        return self.json_data


def mock_requests_get(url, *args, **kwargs):
    if url == 'https://api-staging.jovian.ai/slack/integration_details':
        if kwargs['headers']['Authorization'] == 'Bearer fake_api_key':
            data = {"data": {
                            "slackAccount": {
                                "accountId": 47,
                                "channel": "@rohit",
                                "deleted": False,
                                "id": 10,
                                "updatedAt": "Fri, 13 Dec 2019 13:41:27 GMT",
                                "workspace": "jovian.ml"
                            }
                        },
                        "success": True }
            
            return MockResponse(data, status_code=200)
        
        elif kwargs['headers']['Authorization'] == 'Bearer fake_api_key_error':
            data = { "errors": [
                            {
                                "code": 200,
                                "message": "Invalid guest key"
                            }
                        ],
                        "success": False }
            return MockResponse(data, 200)

        else:
            data = { "errors": [
                            {
                                "code": 401,
                                "message": "Missing Authorization Header"
                            }
                        ],
                        "success": False }
            return MockResponse(data, 401)

def mock_requests_post(url, *args, **kwargs):
    if url == 'https://api-staging.jovian.ai/slack/notify':
        # check for correct api key
        if kwargs['headers']['Authorization'] == 'Bearer fake_api_key':
            data = { 
                "data": {
                            "messageId": "60023f08f3b54801bd58cf6b37067ed6",
                            "messageSent": True
                        },
                "success": True 
            }
            return MockResponse(data, 200)
        elif kwargs['headers']['Authorization'] == 'Bearer fake_invalid_api_key':
            data = {
                "errors": [
                    {
                        "code": 401,
                        "message": "The token is invalid"
                    }
                ],
                "success": False
            }

            return MockResponse(data, 401)

        elif kwargs['headers']['Authorization'] == 'Bearer fake_expired_api_key':
            data = {
                "errors": [
                    {
                        "code": 200,
                        "message": "The token has expired"
                    }
                ],
                "success": False
            }

            return MockResponse(data, 200)


@mock.patch("jovian.utils.slack.get", side_effect=mock_requests_get)
def test_add_slack(mock_get, capsys):
    with fake_creds('.jovian-add-slack', 'credentials.json', purge=True):
        # setUp
        creds = { "WEBAPP_URL": "https://staging.jovian.ml/",
                "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                "API_URL": "https://api-staging.jovian.ai",
                "API_KEY": "fake_api_key",
                "ORG_ID": "staging" }
        write_creds(creds)

        add_slack()

        captured = capsys.readouterr()

        assert captured.out.strip() == "[jovian] Slack already connected." + \
                                       " \nWorkspace: jovian.ml\nConnected Channel: @rohit"

@mock.patch("jovian.utils.slack.get", side_effect=mock_requests_get)
def test_add_slack_errors(mock_get, capsys):
    with fake_creds('.jovian-add-slack', 'credentials.json', purge=True):
        # setUp
        creds = { "WEBAPP_URL": "https://staging.jovian.ml/",
                "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                "API_URL": "https://api-staging.jovian.ai",
                "API_KEY": "fake_api_key_error",
                "ORG_ID": "staging"  }
        write_creds(creds)

        add_slack()

        captured = capsys.readouterr()

        assert captured.out.strip() == "[jovian] Invalid guest key"


class TestAddSlack(TestCase):
    @mock.patch("jovian.utils.slack.get", side_effect=mock_requests_get)
    def test_add_slack_api_error(self, mock_get):
        with fake_creds('.jovian-add-slack', 'credentials.json', purge=True):
            # setUp
            creds = { "WEBAPP_URL": "https://staging.jovian.ml/",
                    "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                    "API_URL": "https://api-staging.jovian.ai",
                    "API_KEY": "fake_invalid_api_key",
                    "ORG_ID": "staging" }
            write_creds(creds)

            with self.assertRaises(ApiError) as context:
                add_slack()

@mock.patch("requests.post", side_effect=mock_requests_post)
def test_notify(mock_requests_post, capsys):
    with fake_creds('.jovian-notify', 'credentials.json', purge=True):
        # setUp
        creds = { "WEBAPP_URL": "https://staging.jovian.ml/",
                "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                "API_URL": "https://api-staging.jovian.ai",
                "API_KEY": "fake_api_key",
                "ORG_ID": "staging" }
        write_creds(creds)

        data = { 'key' : 'value' }
        notify(data)

        captured = capsys.readouterr()

        assert captured.out.strip() == "[jovian] message_sent:True"

@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_notify_safe_true(mock_requests_post, mock_get_api_key, capsys):
    with fake_creds('.jovian-notify', 'credentials.json', purge=True):
        # setUp
        creds = { "WEBAPP_URL": "https://staging.jovian.ml/",
                "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                "API_URL": "https://api-staging.jovian.ai",
                "API_KEY": "fake_invalid_api_key",
                "ORG_ID": "staging" }
        write_creds(creds)

        data = { 'key' : 'value' }
        notify(data, safe=True)

        captured = capsys.readouterr()

        assert captured.out.strip() == "[jovian] message_sent:False"

@mock.patch("requests.post", side_effect=mock_requests_post)
def test_notify_log_error(mock_requests_post, capsys):
    with fake_creds('.jovian-notify', 'credentials.json', purge=True):
        # setUp
        creds = { "WEBAPP_URL": "https://staging.jovian.ml/",
                "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                "API_URL": "https://api-staging.jovian.ai",
                "API_KEY": "fake_expired_api_key",
                "ORG_ID": "staging" }
        write_creds(creds)

        data = { 'key' : 'value' }
        notify(data)

        captured = capsys.readouterr()

        assert captured.err.strip() == "[jovian] Error: The token has expired"


class TestNotify(TestCase):
    @mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
    @mock.patch("requests.post", side_effect=mock_requests_post)
    def test_notify_safe_false_raises_api_error(self, mock_requests_post, mock_get_api_key):
        with fake_creds('.jovian-notify', 'credentials.json', purge=True):
            # setUp
            creds = { "WEBAPP_URL": "https://staging.jovian.ml/",
                    "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                    "API_URL": "https://api-staging.jovian.ai",
                    "API_KEY": "fake_invalid_api_key",
                    "ORG_ID": "staging" }
            write_creds(creds)

            data = { 'key' : 'value' }
            with self.assertRaises(ApiError) as context:
                notify(data)
