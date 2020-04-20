import json
from unittest import TestCase, mock

from jovian.tests.resources.shared import MockResponse, fake_creds
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


@mock.patch('requests.get', side_effect=mocked_requests)
def test_get(mock_get):
    expected_result = {'key': 'value'}

    assert get('http://someurl.com/test.json', headers={'key': 'value'}).json() == expected_result


@mock.patch('requests.get', side_effect=mocked_requests)
def test_get_called_once(mock_get):
    get('http://someurl.com/test.json', headers={'key': 'value'})

    assert mock_get.call_count == 1


@mock.patch('jovian.utils.request.get_api_key', mock.Mock(return_value="fake_api_key"))
@mock.patch('requests.get', side_effect=mocked_requests)
def test_get_called_twice(mock_get):
    get('http://someurl.com/noauth', headers={'key': 'value'})

    assert mock_get.call_count == 2


@mock.patch('requests.post', side_effect=mocked_requests)
def test_post(mock_post):
    expected_result = {"message": "created successfully"}

    assert post('http://someurl.com/create', headers={'key': 'value'}).json() == expected_result


@mock.patch('requests.post', side_effect=mocked_requests)
def test_post_called_once(mock_post):
    post('http://someurl.com/create', headers={'key': 'value'})

    assert mock_post.call_count == 1


@mock.patch('jovian.utils.request.get_api_key', mock.Mock(return_value="fake_api_key"))
@mock.patch('requests.post', side_effect=mocked_requests)
def test_post_called_twice(mock_post):
    post('http://someurl.com/noauth', headers={'key': 'value'})

    assert mock_post.call_count == 2
