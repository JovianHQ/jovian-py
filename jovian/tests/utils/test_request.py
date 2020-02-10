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


def mocked_requests(url, *args, **kwargs):

    if url == 'http://someurl.com/test.json':
        return MockResponse({'key': 'value'}, 200)
    elif url == 'http://someurl.com/noauth':
        return MockResponse({'message': 'invalid creds'}, 401)
    elif url == 'http://someurl.com/create':
        return MockResponse({'message': 'created successfully'}, 201)
    return MockResponse(None, 404)


class TestGet(TestCase):

    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_get(self, mock_get):
        expected_result = {'key': 'value'}

        self.assertEqual(get('http://someurl.com/test.json', headers={'key': 'value'}).json(), expected_result)

    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_get_called_once(self, mock_get):
        get('http://someurl.com/test.json', headers={'key': 'value'})

        assert mock_get.call_count == 1

    @mock.patch('jovian.utils.request.get_api_key', mock.Mock(return_value="fake_api_key"))
    @mock.patch('requests.get', side_effect=mocked_requests)
    def test_get_called_twice(self, mock_get):
        get('http://someurl.com/noauth', headers={'key': 'value'})

        assert mock_get.call_count == 2


class TestPost(TestCase):

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_get(self, mock_post):
        expected_result = {"message": "created successfully"}

        self.assertEqual(post('http://someurl.com/create', headers={'key': 'value'}).json(), expected_result)

    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_post_called_once(self, mock_post):
        post('http://someurl.com/create', headers={'key': 'value'})

        assert mock_post.call_count == 1

    @mock.patch('jovian.utils.request.get_api_key', mock.Mock(return_value="fake_api_key"))
    @mock.patch('requests.post', side_effect=mocked_requests)
    def test_post_called_twice(self, mock_post):
        post('http://someurl.com/noauth', headers={'key': 'value'})

        assert mock_post.call_count == 2
