import os
from unittest import TestCase, mock
from uuid import UUID

import pytest

from jovian.tests.resources.shared import MockResponse, fake_creds
from jovian.utils import credentials
from jovian.utils.credentials import (API_TOKEN_KEY, GUEST_TOKEN_KEY, _generate_guest_key, _read_or_generate_guest_key,
                                      _u, _validate_guest_key, config_exists, creds_exist, ensure_org, get_api_key,
                                      get_creds_path, get_guest_key, init_config, purge_api_key, purge_config,
                                      purge_cred_key, purge_creds, read_api_key_opt, read_api_url, read_cred,
                                      read_creds, read_or_request_api_key, read_org_id, read_webapp_url,
                                      request_api_key, request_org_id, validate_api_key, write_api_key, write_api_url,
                                      write_cred, write_creds, write_guest_key, write_org_id, write_webapp_url)
from jovian.utils.error import ApiError, ConfigError

try:
    # Python 3
    from json.decoder import JSONDecodeError
except ImportError:
    # Python 2
    JSONDecodeError = ValueError


def test_config_exits_false():
    with fake_creds():
        purge_config()
        assert config_exists() == False


def test_config_exists_true():
    with fake_creds():
        assert config_exists() == True


def test_purge_config():
    with fake_creds():
        os.makedirs(credentials.CONFIG_DIR, exist_ok=True)
        assert config_exists() == True
        purge_config()
        assert config_exists() == False


def test_get_creds_path():
    with fake_creds() as dir:
        assert get_creds_path() == os.path.join(dir, '.jovian/credentials.json')


def test_init_config():
    with fake_creds() as dir:
        init_config()
        assert os.path.exists(os.path.join(dir, '.jovian')) == True


def test_purge_creds():
    with fake_creds() as dir:
        assert os.path.exists(os.path.join(dir, '.jovian/credentials.json')) == True
        purge_creds()
        assert os.path.exists(os.path.join(dir, '.jovian/credentials.json')) == False


def test_purge_api_key():
    with fake_creds():
        assert read_cred(API_TOKEN_KEY) == 'fake_api_key'

        purge_api_key()

        with pytest.raises(KeyError):
            read_cred(API_TOKEN_KEY)


def test_read_creds_no_creds_folder():
    with fake_creds():
        purge_creds()
        assert read_creds() == {}


def test_read_creds_folder_exists():
    with fake_creds():
        expected_result = {"WEBAPP_URL": "https://staging.jovian.ml/",
                           "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                           "ORG_ID": "staging",
                           "API_URL": "https://api-staging.jovian.ai",
                           "API_KEY": "fake_api_key"}
        assert read_creds() == expected_result


def mock_json_load(*args, **kwargs):
    raise ValueError('fake value error')


@mock.patch("jovian.utils.credentials.purge_creds", return_value=None)
@mock.patch("json.load", side_effect=mock_json_load)
def test_read_creds_with_value_error(mock_json_load, mock_purge_creds):
    with fake_creds():
        assert read_creds() == {}


def test_creds_exist_true():
    with fake_creds():
        assert creds_exist() == True


def test_creds_exist_false():
    with fake_creds():
        purge_api_key()

        assert creds_exist() == False


def test_read_cred_no_default():
    with fake_creds():
        assert read_cred('ORG_ID') == 'staging'


def test_read_cred_with_default():
    with fake_creds():
        assert read_cred('FAKE_ID', 'default_value') == 'default_value'


def test_write_creds():
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        assert read_creds() == creds


def test_write_cred():
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        write_cred('FAKE_KEY', 'fake_value')

        expected_result = {"WEBAPP_URL": "https://staging.jovian.ml/",
                           "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                           "ORG_ID": "staging",
                           "API_URL": "https://api-staging.jovian.ai",
                           "FAKE_KEY": "fake_value"}
        assert read_creds() == expected_result


def test_write_cred_already_exists():
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        write_cred('ORG_ID', 'staging')

        expected_result = creds
        assert read_creds() == expected_result


def test_purge_cred_key():
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        purge_cred_key('GUEST_KEY')

        expected_result = {"WEBAPP_URL": "https://staging.jovian.ml/",
                           "ORG_ID": "staging",
                           "API_URL": "https://api-staging.jovian.ai"}

        assert read_creds() == expected_result


def test_write_api_url():
    with fake_creds():
        write_api_url("https://fake_api.jovian.ai/")

        from jovian.utils.credentials import API_URL_KEY
        assert read_cred(API_URL_KEY) == "https://fake_api.jovian.ai/"


def test_read_api_url():
    with fake_creds():
        write_api_url("https://fake_api.jovian.ai/")
        assert read_api_url() == "https://fake_api.jovian.ai/"


def test_write_org_id():
    with fake_creds():
        write_org_id("fake_org_id")

        from jovian.utils.credentials import ORG_ID_KEY
        assert read_cred(ORG_ID_KEY) == "fake_org_id"


def test_read_org_id():
    with fake_creds():
        write_org_id("fake_org_id")
        assert read_org_id() == "fake_org_id"


def test_write_webapp_url():
    with fake_creds():
        write_webapp_url("http://fake-webapp-url.ai/")

        from jovian.utils.credentials import WEBAPP_URL_KEY
        assert read_cred(WEBAPP_URL_KEY) == "http://fake-webapp-url.ai/"


def test_read_webapp_url():
    with fake_creds():
        write_webapp_url("http://fake-webapp-url.ai/")
        assert read_webapp_url() == "http://fake-webapp-url.ai/"


@mock.patch("click.prompt", return_value="fake_org_id")
def test_request_org_id(mock_prompt):
    assert request_org_id() == "fake_org_id"


def mock_requests_get(url, *args, **kwargs):
    if url == 'https://jovian.ml/config.json':
        data = {"API_URL": "https://api.jovian.ai"}

        return MockResponse(data, status_code=200)

    elif url == 'https://fakecompany.jovian.ml/config.json':

        return MockResponse({"msg": "Request failed"}, status_code=500, text="Fake internal server error")

    elif url == 'https://jsonerror.jovian.ml/config.json':
        data = {"API_URL": "https://api.jovian.ai"}
        res = MockResponse(data, status_code=200, text="response of fake json decode error")
        res.json = json_decode_error_raiser

        return res

    elif url == 'https://no-api-key.jovian.ml/config.json':
        data = {}

        return MockResponse(data, status_code=200, text="response with no api key")

    elif url == 'https://api-staging.jovian.ai/user/profile':
        key = kwargs['headers']['Authorization']
        if key == 'Bearer fake_correct_auth_key':
            return MockResponse({'key': 'value'}, 200)

        return MockResponse({'key': 'value'}, 401)


def connection_error_raiser(*args, **kwargs):
    raise ConnectionError('fake connection error')


def json_decode_error_raiser(*args, **kwargs):
    raise JSONDecodeError('fake json decode error', 'credentials.json', 0)


@mock.patch("jovian.utils.credentials.is_flavor_pro", return_value=True)
def test_ensure_org_all_creds_exist(mock_is_flavor_pro):
    with fake_creds():
        assert ensure_org() == None


@mock.patch("requests.get", side_effect=mock_requests_get)
@mock.patch("jovian.utils.credentials.request_org_id", return_value="")
@mock.patch("jovian.utils.credentials.is_flavor_pro", return_value=True)
def test_ensure_org_some_creds_exist_default_org_id(
        mock_is_flavor_pro, mock_request_org_id, mock_requests_get):
    with fake_creds():
        # setUp
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "GUEST_KEY": "b6538d4dfde04fcf993463a828a9cec6",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        ensure_org()

        assert read_api_url() == "https://api.jovian.ai"
        assert read_org_id() == "public"
        assert read_webapp_url() == "https://jovian.ml/"


@pytest.mark.parametrize(
    "get_side_effect, request_org_id, creds, msg",
    [
        (
            connection_error_raiser,
            "fakecompany",
            {"WEBAPP_URL": "https://staging.jovian.ml/",
             "API_URL": "https://api-staging.jovian.ai"},
            "Failed to connect to https://fakecompany.jovian.ml/ . Please verify your organization ID and " +
            "ensure you are connected to the internet."
        ),
        (
            mock_requests_get,
            "fakecompany",
            {"WEBAPP_URL": "https://staging.jovian.ml/",
             "API_URL": "https://api-staging.jovian.ai"},
            "Request to retrieve configuration file https://fakecompany.jovian.ml/config.json failed with " +
            "status_code 500 . Looks like there's something wrong with your setup.",
        ),
        (
            mock_requests_get,
            "jsonerror",
            {"WEBAPP_URL": "https://staging.jovian.ml/",
             "API_URL": "https://api-staging.jovian.ai"},
            "Failed to parse JSON configuration file from https://jsonerror.jovian.ml/config.json",
        ),
        (
            mock_requests_get,
            "no-api-key",
            {"WEBAPP_URL": "https://staging.jovian.ml/"},
            "Failed to extract API_URL from JSON configuration file https://no-api-key.jovian.ml/config.json"
        ),
    ]
)
@mock.patch("jovian.utils.credentials.is_flavor_pro", return_value=True)
def test_ensure_org_pro_raises_error(mock_is_flavor_pro, get_side_effect, request_org_id, creds, msg):
    with fake_creds(), \
            mock.patch("jovian.utils.credentials.request_org_id", return_value=request_org_id), \
            mock.patch("requests.get", side_effect=get_side_effect):

        write_creds(creds)

        with pytest.raises(ConfigError) as context:
            ensure_org()

        assert msg in str(context.value)


def test_write_api_key():
    with fake_creds():
        write_api_key("fake_api_key")

        from jovian.utils.credentials import API_TOKEN_KEY
        assert read_cred(API_TOKEN_KEY) == "fake_api_key"


@pytest.mark.parametrize(
    "api_key, expected_result",
    [
        ("fake_correct_auth_key", True),
        ("fake_invalid_auth_key", False),
    ]
)
@mock.patch("requests.get", side_effect=mock_requests_get)
def test_validate_api_key(mock_requests_get, api_key, expected_result):
    with fake_creds():
        assert validate_api_key(api_key) == expected_result


def test_write_guest_key():
    with fake_creds():
        write_guest_key("fake_guest_key")

        from jovian.utils.credentials import GUEST_TOKEN_KEY
        assert read_cred(GUEST_TOKEN_KEY) == "fake_guest_key"


@mock.patch("click.prompt", return_value="fake_api_key")
def test_request_api_key(mock_prompt):
    assert request_api_key() == "fake_api_key"


def test_read_api_key_opt():
    with fake_creds():
        assert read_api_key_opt() == ('fake_api_key', 'read')


def test_read_api_key_opt_none():
    with fake_creds():
        purge_api_key()

        assert read_api_key_opt() == (None, 'read')


def test_read_or_request_api_key():
    with fake_creds():
        assert read_or_request_api_key() == ('fake_api_key', 'read')


@mock.patch("click.prompt", return_value="fake_api_key")
def test_read_or_request_api_key_none(mock_prompt):
    with fake_creds():
        purge_api_key()

        assert read_or_request_api_key() == ('fake_api_key', 'request')


@mock.patch("uuid.uuid4", return_value=UUID('b66406dc-02c3-471b-ac27-d923fb4c6b1e'))
def test_generate_guest_key(mock_uuid4):
    assert _generate_guest_key() == 'b66406dc02c3471bac27d923fb4c6b1e'


def test_read_or_generate_guest_key():
    with fake_creds():
        assert _read_or_generate_guest_key() == "b6538d4dfde04fcf993463a828a9cec6"


@mock.patch("uuid.uuid4", return_value=UUID('b66406dc-02c3-471b-ac27-d923fb4c6b1e'))
def test_read_or_generate_guest_key_generate(mock_uuid4):
    with fake_creds():
        purge_cred_key(GUEST_TOKEN_KEY)
        assert _read_or_generate_guest_key() == "b66406dc02c3471bac27d923fb4c6b1e"


def test_validate_guest_key():
    assert _validate_guest_key("b6538d4dfde04fcf993463a828a9cec6") == True
    assert _validate_guest_key("fake-uuid-key") == False


def test_get_guest_key():
    with fake_creds():
        assert get_guest_key() == "b6538d4dfde04fcf993463a828a9cec6"


@mock.patch("uuid.uuid4", return_value=UUID('b66406dc-02c3-471b-ac27-d923fb4c6b1e'))
def test_get_guest_key_generate_key(mock_uuid4):
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        assert get_guest_key() == "b66406dc02c3471bac27d923fb4c6b1e"


@mock.patch("jovian.utils.credentials.validate_api_key", return_value=True)
def test_get_api_key(mock_validate_api_key):
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "ORG_ID": "staging",
                 "API_KEY": "fake_api_key",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        assert get_api_key() == "fake_api_key"


@mock.patch("click.prompt", return_value="fake_api_key")
@mock.patch("jovian.utils.credentials.validate_api_key", return_value=False)
def test_get_api_key_api_error(mock_validate_api_key, mock_prompt):
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        with pytest.raises(ApiError):
            get_api_key()


@mock.patch("click.prompt", return_value="fake_api_key")
@mock.patch("jovian.utils.credentials.validate_api_key", return_value=True)
def test_get_api_key_request_once(mock_validate_api_key, mock_prompt):
    with fake_creds():
        creds = {"WEBAPP_URL": "https://staging.jovian.ml/",
                 "ORG_ID": "staging",
                 "API_URL": "https://api-staging.jovian.ai"}
        write_creds(creds)

        assert get_api_key() == "fake_api_key"
