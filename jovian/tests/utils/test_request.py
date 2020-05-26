import json
from unittest import TestCase, mock

import pytest

from jovian.tests.resources.shared import MockResponse
from jovian.utils.request import _msg, get, post, pretty, retry


def test_msg_errors():
    mock_res = mock.Mock()
    mock_res.json.return_value = {
        'errors': [
            {
                'message': 'this is a fake requests error',
                'code': 400
            }
        ]
    }

    expected_result = 'this is a fake requests error'
    assert _msg(mock_res) == expected_result


def test_msg_message():
    mock_res = mock.Mock()
    mock_res.json.return_value = {
        'message': 'this is a fake response message'
    }

    expected_result = 'this is a fake response message'
    assert _msg(mock_res) == expected_result


def test_msg_msg():
    mock_res = mock.Mock()
    mock_res.json.return_value = {
        'msg': 'this is a fake response message'
    }

    expected_result = 'this is a fake response message'
    assert _msg(mock_res) == expected_result


def test_msg_exception_text():
    mock_res = mock.Mock(return_value=ValueError('fake value error'))
    mock_res.text = 'this is a fake response text'

    expected_result = 'this is a fake response text'
    assert _msg(mock_res) == expected_result


def test_msg_exception_no_text():
    mock_res = mock.Mock()
    mock_res.json.return_value = ValueError('fake value error')
    mock_res.text = ''
    expected_result = 'Something went wrong'
    assert _msg(mock_res) == expected_result


def test_pretty():
    mock_res = mock.Mock()
    mock_res.status_code = 200
    mock_res.json.return_value = {
        'msg': 'this is a fake response message'
    }

    expected_result = '(HTTP 200) this is a fake response message'
    assert pretty(mock_res) == expected_result


def mocked_requests(url, *args, **kwargs):
    if url == 'http://someurl.com/test.json':
        return MockResponse({'key': 'value'}, 200)
    elif url == 'http://someurl.com/noauth':
        return MockResponse({'message': 'invalid creds'}, 401)
    elif url == 'http://someurl.com/create':
        return MockResponse({'message': 'created successfully'}, 201)
    return MockResponse(None, 404)


@pytest.mark.parametrize(
    "func, url, req, ret_val_api_key, call_count",
    [
        (
            get,
            "http://someurl.com/test.json",
            "requests.get",
            None,
            1
        ),
        (
            get,
            "http://someurl.com/noauth",
            "requests.get",
            "fake_api_key",
            2
        ),
        (
            post,
            "http://someurl.com/noauth",
            "requests.post",
            "fake_api_key",
            2
        ),
        (
            post,
            "http://someurl.com/create",
            "requests.post",
            None,
            1
        ),
    ]
)
def test_request(func, url, req, ret_val_api_key, call_count):
    with mock.patch(req, side_effect=mocked_requests) as mock_req, \
            mock.patch('jovian.utils.request.get_api_key', return_value=ret_val_api_key):

        func(url, headers={'key': 'value'})
        assert mock_req.call_count == call_count
