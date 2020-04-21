import os
from unittest import TestCase, mock
from unittest.mock import ANY

import pytest

from jovian.tests.resources.shared import MockResponse, fake_creds
from jovian._version import __version__
from jovian.utils.api import (
    _h,
    create_gist_simple,
    get_current_user,
    get_gist,
    get_gist_access,
    post_block,
    post_blocks,
    post_records,
    post_slack_message,
    upload_file,
)
from jovian.utils.credentials import write_creds
from jovian.utils.error import ApiError


def mock_requests_post(url, *args, **kwargs):
    if (
        url == "https://api-staging.jovian.ai/gist/create"
        or url == "https://api-staging.jovian.ai/gist/fake_gist_slug/upload"
    ):
        if kwargs["headers"]["Authorization"] == "Bearer fake_api_key":
            data = {"data": {"message": "Gist created successfully"}}
            return MockResponse(data, status_code=200)
        else:
            data = {
                "errors": [{"code": 404, "message": "Gist not found"}],
                "success": False,
            }
            return MockResponse(data, status_code=404)
    elif url == "https://api-staging.jovian.ai/data/record":
        if kwargs["headers"]["Authorization"] == "Bearer fake_api_key":
            data = {"data": {"message": "Data logged successfully"}}
            return MockResponse(data, status_code=200)
        else:
            data = {
                "errors": [{"code": 500, "message": "Internal Server Error"}],
                "success": False,
            }
            return MockResponse(data, status_code=500)

    elif url == "https://api-staging.jovian.ai/data/fake_gist_slug/commit":
        if kwargs["headers"]["Authorization"] == "Bearer fake_api_key":
            data = {"data": {"message": "Data logged successfully"}}
            return MockResponse(data, status_code=200)
        else:
            data = {
                "errors": [{"code": 404, "message": "Gist not found"}],
                "success": False,
            }
            return MockResponse(data, status_code=404)

    elif url == "https://api-staging.jovian.ai/slack/notify":
        if kwargs["headers"]["Authorization"] == "Bearer fake_api_key":
            data = {
                "data": {
                    "messageId": "60023f08f3b54801bd58cf6b37067ed6",
                    "messageSent": True,
                },
                "success": True,
            }
            return MockResponse(data, 200)
        elif kwargs["headers"]["Authorization"] == "Bearer fake_invalid_api_key":
            data = {
                "errors": [{"code": 401, "message": "The token is invalid"}],
                "success": False,
            }

            return MockResponse(data, 401)

        elif kwargs["headers"]["Authorization"] == "Bearer fake_expired_api_key":
            data = {
                "errors": [{"code": 200, "message": "The token has expired"}],
                "success": False,
            }

            return MockResponse(data, 200)


def mock_requests_get(url, *args, **kwargs):
    if url == "https://api-staging.jovian.ai/user/profile":
        if kwargs["headers"]["Authorization"] == "Bearer fake_api_key":
            data = {"data": {"id": 47, "username": "rohit"}, "success": True}

            return MockResponse(data, status_code=200)
        else:
            data = {
                "errors": [{"code": 401, "message": "Signature verification failed"}],
                "success": False,
            }
            return MockResponse(data, status_code=401)

    elif (
        url == "https://api-staging.jovian.ai/user/rohit/gist/demo-notebook"
        or url
        == "https://api-staging.jovian.ai/user/rohit/gist/demo-notebook?gist_version=3"
        or url == "https://api-staging.jovian.ai/gist/f67108fc906341d8b15209ce88ebc3d2"
    ):

        data = {
            "data": {
                "archived": False,
                "clonesCount": 0,
                "createdAt": 1578718557994,
                "currentUser": {"id": 47, "username": "rohit"},
                "deleted": False,
                "description": None,
            }
        }

        return MockResponse(data, status_code=200)

    # Dictionary containing mock responses
    response_dict = {
        "https://api-staging.jovian.ai/gist/fake_nonexistent_gist": MockResponse(
            {"errors": [{"code": 404, "message": "Gist not found"}], "success": False},
            status_code=404,
        ),
        "https://api-staging.jovian.ai/gist/fake_gist_too_large": MockResponse(
            {"message": "Internal Server Error"}, status_code=500
        ),
        "https://api-staging.jovian.ai/gist/f67108fc906341d8b15209ce88ebc3d2/check-access": MockResponse(
            {
                "data": {
                    "currentUser": {"id": 47, "username": "rohit"},
                    "read": True,
                    "slug": "f67108fc906341d8b15209ce88ebc3d2",
                    "write": True,
                },
                "success": True,
            },
            status_code=200,
        ),
        "https://api-staging.jovian.ai/gist/fake_nonexistent_gist/check-access": MockResponse(
            {"errors": [{"code": 404, "message": "Gist not found"}], "success": False},
            status_code=404,
        ),
    }

    return response_dict[url]


def test_h():
    with fake_creds():
        expected_result = {
            "Authorization": "Bearer fake_api_key",
            "x-jovian-source": "library",
            "x-jovian-library-version": __version__,
            "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
            "x-jovian-org": "staging",
        }

        assert _h() == expected_result


@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_current_user(mock_requests_get):
    with fake_creds():
        get_current_user()

        mock_requests_get.assert_called_with(
            "https://api-staging.jovian.ai/user/profile",
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            params=None,
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_current_user_raises_exception(
    mock_requests_get, mock_request_get_api_key
):
    with fake_creds():
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        with pytest.raises(Exception) as context:
            get_current_user()

        mock_requests_get.assert_called_with(
            "https://api-staging.jovian.ai/user/profile",
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            params=None,
        )

        assert (
            str(context.value)
            == "Failed to fetch current user profile. (HTTP 401) Signature verification failed"
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_gist(mock_requests_get, mock_request_get_api_key):
    with fake_creds():
        get_gist("rohit/demo-notebook")
        mock_requests_get.assert_called_with(
            "https://api-staging.jovian.ai/user/rohit/gist/demo-notebook",
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            params=None,
        )

        get_gist("rohit/demo-notebook", version=3)
        mock_requests_get.assert_called_with(
            "https://api-staging.jovian.ai/user/rohit/gist/demo-notebook?gist_version=3",
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            params=None,
        )

        get_gist("f67108fc906341d8b15209ce88ebc3d2")
        mock_requests_get.assert_called_with(
            "https://api-staging.jovian.ai/gist/f67108fc906341d8b15209ce88ebc3d2",
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            params=None,
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_gist_not_found(mock_requests_get, mock_get_api_key):
    with fake_creds():
        assert get_gist("fake_nonexistent_gist") == False


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_gist_raises_exception(mock_requests_get, mock_get_api_key):
    with fake_creds():
        with pytest.raises(Exception) as context:
            get_gist("fake_gist_too_large")

        assert (
            str(context.value)
            == 'Failed to retrieve metadata for notebook "fake_gist_too_large":'
            + " (HTTP 500) Internal Server Error"
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_gist_access(mock_requests_get, mock_get_api_key):
    with fake_creds():
        get_gist_access("f67108fc906341d8b15209ce88ebc3d2")
        mock_requests_get.assert_called_with(
            "https://api-staging.jovian.ai/gist/f67108fc906341d8b15209ce88ebc3d2/check-access",
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            params=None,
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_api_key")
@mock.patch("requests.get", side_effect=mock_requests_get)
def test_get_gist_access_raises_exception(
    mock_requests_get, mock_get_api_key
):
    with fake_creds():
        with pytest.raises(Exception) as context:
            get_gist_access("fake_nonexistent_gist")

        mock_requests_get.assert_called_with(
            "https://api-staging.jovian.ai/gist/fake_nonexistent_gist/check-access",
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            params=None,
        )

        assert (
            str(context.value)
            == "Failed to retrieve access permission for notebook"
            + ' "fake_nonexistent_gist" (retry with new_project=True to create a new notebook):'
            + " (HTTP 404) Gist not found"
        )


@mock.patch("requests.post", side_effect=mock_requests_post)
def test_create_gist_simple_no_gist_slug(mock_requests_post):
    with fake_creds() as dir:
        create_gist_simple(
            filename=os.path.join(dir, ".jovian/credentials.json"),
            title="Credentials",
            privacy="private",
            version_title="first version",
        )

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/gist/create",
            data={
                "visibility": "private",
                "public": False,
                "title": "Credentials",
                "version_title": "first version",
            },
            files={
                "files": (
                    os.path.join(dir, ".jovian/credentials.json"),
                    ANY,
                )
            },
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=None,
        )


@mock.patch("requests.post", side_effect=mock_requests_post)
def test_create_gist_simple_with_gist_slug(mock_requests_post):
    with fake_creds() as dir:
        create_gist_simple(
            filename=os.path.join(dir, ".jovian/credentials.json"),
            gist_slug="fake_gist_slug",
            title="Credentials",
            version_title="first version",
        )

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/gist/fake_gist_slug/upload",
            data={"version_title": "first version"},
            files={
                "files": (
                    os.path.join(dir, ".jovian/credentials.json"),
                    ANY,
                )
            },
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=None,
        )


@mock.patch("requests.post", side_effect=mock_requests_post)
def test_create_gist_simple_raises_api_error(mock_requests_post):
    with fake_creds() as dir:
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        with pytest.raises(ApiError) as context:
            create_gist_simple(
                filename=os.path.join(dir, ".jovian/credentials.json"),
                title="Credentials",
                version_title="first version",
            )

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/gist/create",
            data={
                "visibility": "auto",
                "public": True,
                "title": "Credentials",
                "version_title": "first version",
            },
            files={
                "files": (
                    os.path.join(dir, ".jovian/credentials.json"),
                    ANY,
                )
            },
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=None,
        )

        assert (
            str(context.value)
            == "File upload failed: (HTTP 404) Gist not found"
        )


@mock.patch("requests.post", side_effect=mock_requests_post)
def test_upload_file(mock_requests_post):
    with fake_creds() as dir:
        with open(
            os.path.join(dir, ".jovian/credentials.json"), "rb"
        ) as f:
            upload_file(
                gist_slug="fake_gist_slug",
                file=("credentials.json", f),
                folder=".jovian",
                artifact=True,
                version_title="fake_version_title",
            )

            mock_requests_post.assert_called_with(
                "https://api-staging.jovian.ai/gist/fake_gist_slug/upload",
                data={
                    "artifact": "true",
                    "folder": ".jovian",
                    "version_title": "fake_version_title",
                },
                files={"files": ("credentials.json", ANY)},
                headers={
                    "Authorization": "Bearer fake_api_key",
                    "x-jovian-source": "library",
                    "x-jovian-library-version": __version__,
                    "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                    "x-jovian-org": "staging",
                },
                json=None,
            )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_upload_file_raises_api_error(mock_requests_post, mock_get_api_key):
    with fake_creds() as dir:
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        with pytest.raises(ApiError) as context:
            with open(
                os.path.join(dir, ".jovian/credentials.json"), "rb"
            ) as f:
                upload_file(
                    gist_slug="fake_gist_slug",
                    file=("credentials.json", f),
                    folder=".jovian",
                    artifact=True,
                    version_title="fake_version_title",
                )

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/gist/fake_gist_slug/upload",
            data={
                "artifact": "true",
                "folder": ".jovian",
                "version_title": "fake_version_title",
            },
            files={"files": ("credentials.json", ANY)},
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=None,
        )

        assert (
            str(context.value)
            == "File upload failed: (HTTP 404) Gist not found"
        )


@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_blocks(mock_requests_post):

    with fake_creds():
        blocks = [{"data": {"key": "value"}, "record_type": "metrics"}]
        post_blocks(blocks)

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/data/record",
            data=None,
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=[{"data": {"key": "value"}, "record_type": "metrics"}],
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_blocks_raises_api_error(mock_requests_post, mock_get_api_key):
    with fake_creds():
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        blocks = [{"data": {"key": "value"}, "record_type": "metrics"}]

        with pytest.raises(ApiError) as context:
            post_blocks(blocks)

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/data/record",
            data=None,
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=[{"data": {"key": "value"}, "record_type": "metrics"}],
        )

        assert (
            str(context.value)
            == "Data logging failed: (HTTP 500) Internal Server Error"
        )


@mock.patch("jovian.utils.api.timestamp_ms", return_value=1582550133094)
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_block(mock_requests_post, mock_timestamp):
    with fake_creds():
        post_block("metrics", {"key": "value"})

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/data/record",
            data=None,
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=[
                {
                    "localTimestamp": 1582550133094,
                    "data": "metrics",
                    "recordType": {"key": "value"},
                }
            ],
        )


@mock.patch("jovian.utils.api.timestamp_ms", return_value=1582550133094)
@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_block_raises_api_error(
    mock_requests_post, mock_get_api_key, mock_timestamp
):
    with fake_creds():
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        with pytest.raises(ApiError) as context:
            post_block("metrics", {"key": "value"})

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/data/record",
            data=None,
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json=[
                {
                    "localTimestamp": 1582550133094,
                    "data": "metrics",
                    "recordType": {"key": "value"},
                }
            ],
        )

        assert (
            str(context.value)
            == "Data logging failed: (HTTP 500) Internal Server Error"
        )


@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_records(mock_requests_post):
    with fake_creds():
        post_records("fake_gist_slug", {"key": "value"})
        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/data/fake_gist_slug/commit",
            data=None,
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json={"key": "value"},
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_records_raises_api_error(mock_requests_post, mock_get_api_key):
    with fake_creds():
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        with pytest.raises(ApiError) as context:
            post_records("fake_gist_slug", {"key": "value"})

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/data/fake_gist_slug/commit",
            data=None,
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json={"key": "value"},
        )

        assert (
            str(context.value)
            == "Data logging failed: (HTTP 404) Gist not found"
        )


@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_slack_message(mock_requests_post):
    with fake_creds():
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        post_slack_message({"key": "value"})

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/slack/notify",
            data=None,
            headers={
                "Authorization": "Bearer fake_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json={"key": "value"},
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_slack_message_raises_api_error(
    mock_requests_post, mock_request_get_api_key
):
    with fake_creds():
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        data = {"key": "value"}

        with pytest.raises(ApiError):
            post_slack_message(data)

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/slack/notify",
            data=None,
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json={"key": "value"},
        )


@mock.patch("jovian.utils.request.get_api_key", return_value="fake_invalid_api_key")
@mock.patch("requests.post", side_effect=mock_requests_post)
def test_post_slack_message_safe(
    mock_requests_post, mock_request_get_api_key
):
    with fake_creds():
        # setUp
        creds = {
            "WEBAPP_URL": "https://staging.jovian.ml/",
            "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
            "API_URL": "https://api-staging.jovian.ai",
            "API_KEY": "fake_invalid_api_key",
            "ORG_ID": "staging",
        }
        write_creds(creds)

        data = {"key": "value"}

        assert post_slack_message(data, safe=True) == {
            "data": {"messageSent": False}
        }

        mock_requests_post.assert_called_with(
            "https://api-staging.jovian.ai/slack/notify",
            data=None,
            headers={
                "Authorization": "Bearer fake_invalid_api_key",
                "x-jovian-source": "library",
                "x-jovian-library-version": __version__,
                "x-jovian-guest": "b6538d4dfde04fcf993463a828a9cec6",
                "x-jovian-org": "staging",
            },
            json={"key": "value"},
        )
