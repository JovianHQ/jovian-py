from unittest import TestCase, mock
from jovian.utils.request import _msg, pretty, get, post, retry
import json


class TestMsg(TestCase):

    def test_msg_errors(self):
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
        self.assertEqual(_msg(mock_res), expected_result)

    def test_msg_message(self):
        mock_res = mock.Mock()
        mock_res.json.return_value = {
            'message': 'this is a fake response message'
        }

        expected_result = 'this is a fake response message'
        self.assertEqual(_msg(mock_res), expected_result)

    def test_msg_msg(self):
        mock_res = mock.Mock()
        mock_res.json.return_value = {
            'msg': 'this is a fake response message'
        }

        expected_result = 'this is a fake response message'
        self.assertEqual(_msg(mock_res), expected_result)

    def test_msg_exception_text(self):
        mock_res = mock.Mock(return_value=ValueError('fake value error'))
        mock_res.text = 'this is a fake response text'

        expected_result = 'this is a fake response text'
        self.assertEqual(_msg(mock_res), expected_result)

    def test_msg_exception_no_text(self):
        mock_res = mock.Mock()
        mock_res.json.return_value = ValueError('fake value error')
        mock_res.text = ''
        expected_result = 'Something went wrong'
        self.assertEqual(_msg(mock_res), expected_result)


class TestPretty(TestCase):

    def test_pretty(self):
        mock_res = mock.Mock()
        mock_res.status_code = 200
        mock_res.json.return_value = {
            'msg': 'this is a fake response message'
        }

        expected_result = '(HTTP 200) this is a fake response message'
        self.assertEqual(pretty(mock_res), expected_result)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mocked_requests_get(url, params=None, **kwargs):

    if url == 'http://someurl.com/test.json':
        return MockResponse({"key1": "value1"}, 200)
    elif url == 'http://someurl.com/noauth':
        return MockResponse({'message': 'invalid creds'}, 401)
    return MockResponse(None, 404)


def mocked_requests_post(url, data=None, json=None, **kwargs):

    if url == 'http://someurl.com/create':
        return MockResponse({"message": "created successfully"}, 201)

    return MockResponse(None, 404)


class TestGet(TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get(self, mock_get):
        expected_result = {"key1": "value1"}

        self.assertEqual(get('http://someurl.com/test.json').json(), expected_result)


class TestPost(TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test_get(self, mock_post):
        expected_result = {"message": "created successfully"}

        self.assertEqual(post('http://someurl.com/create').json(), expected_result)


class TestRetry(TestCase):
    @mock.patch('jovian.utils.request.purge_api_key', mock.Mock(return_value=None))
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_retry_get(self, mocked_requests_get):
        get('http://someurl.com/noauth')

    @mock.patch('jovian.utils.request.get_api_key', mock.Mock(return_value="fake_api_key"))
    @mock.patch('jovian.utils.request.purge_api_key', mock.Mock(return_value=None))
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_retry_get_with_headers(self, mocked_requests_get):
        get('http://someurl.com/noauth', headers={'key': 'value'})

    @mock.patch('jovian.utils.request.purge_api_key', mock.Mock(return_value=None))
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_retry_post(self, mocked_requests_get):
        get('http://someurl.com/noauth')

    @mock.patch('jovian.utils.request.get_api_key', mock.Mock(return_value="fake_api_key"))
    @mock.patch('jovian.utils.request.purge_api_key', mock.Mock(return_value=None))
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_retry_post_with_headers(self, mocked_requests_get):
        get('http://someurl.com/noauth', headers={'key': 'value'})
