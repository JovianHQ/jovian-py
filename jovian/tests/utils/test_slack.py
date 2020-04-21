import os
from unittest import TestCase, mock

import pytest

from jovian._version import __version__
from jovian.tests.resources.shared import MockResponse, fake_creds
from jovian.utils import slack
from jovian.utils.credentials import write_creds
from jovian.utils.error import ApiError
from jovian.utils.slack import _h, add_slack, notify


def test_h():
    with fake_creds():
        expected_result = {
            "Authorization": "Bearer fake_api_key",
            "x-jovian-source": "library",
            "x-jovian-library-version": __version__,
            "x-jovian-command": "add-slack",
            "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
            "x-jovian-org": "staging",
        }

        assert _h() == expected_result


def mock_requests_get(url, *args, **kwargs):
    if url == "https://api-staging.jovian.ai/slack/integration_details":
        if kwargs["headers"]["Authorization"] == "Bearer fake_api_key":
            data = {
                "data": {
                    "slackAccount": {
                        "accountId": 47,
                        "channel": "@rohit",
                        "deleted": False,
                        "id": 10,
                        "updatedAt": "Fri, 13 Dec 2019 13:41:27 GMT",
                        "workspace": "jovian.ml",
                    }
                },
                "success": True,
            }

            return MockResponse(data, status_code=200)

        elif kwargs["headers"]["Authorization"] == "Bearer fake_api_key_error":
            data = {
                "errors": [{"code": 200, "message": "Invalid guest key"}],
                "success": False,
            }
            return MockResponse(data, 200)

        else:
            data = {
                "errors": [{"code": 401, "message": "Missing Authorization Header"}],
                "success": False,
            }
            return MockResponse(data, 401)


@pytest.mark.parametrize(
    "api_key, expected_result",
    [
        (
            "fake_api_key",
            "[jovian] Slack already connected."
            + " \nWorkspace: jovian.ml\nConnected Channel: @rohit"
        ),
        (
            "fake_api_key_error",
            "[jovian] Invalid guest key"
        ),
    ]
)
@mock.patch("jovian.utils.slack.get", side_effect=mock_requests_get)
def test_add_slack(mock_requests_get, api_key, expected_result, capsys):
    with fake_creds():
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": api_key,
            "ORG_ID": "staging",
        }
        write_creds(creds)

        add_slack()

        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.slack.get", side_effect=mock_requests_get)
def test_add_slack_api_error(mock_get):
    with fake_creds():
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        with pytest.raises(ApiError):
            add_slack()


@pytest.mark.parametrize(
    "resp, expected_result, safe",
    [
        (
            {
                "data": {
                    "messageId": "60023f08f3b54801bd58cf6b37067ed6",
                    "messageSent": True,
                },
                "success": True,
            },
            "[jovian] message_sent:True",
            False
        ),
        (
            {
                "errors": [{"code": 401, "message": "The token is invalid"}],
                "success": False,
            },
            "[jovian] Error: The token is invalid",
            True
        ),
        (
            {
                "errors": [{"code": 200, "message": "The token has expired"}],
                "success": False,
            },
            "[jovian] Error: The token has expired",
            False
        ),
    ]
)
def test_notify(resp, expected_result, safe, capsys):
    with mock.patch("jovian.utils.slack.post_slack_message", return_value=resp):
        notify({"key": "value"}, safe=safe)

        captured = capsys.readouterr()
        if "errors" in resp:
            assert captured.err.strip() == expected_result
        else:
            assert captured.out.strip() == expected_result
