from functools import wraps

import requests

from jovian.utils.credentials import get_api_key, purge_api_key
from jovian.utils.logger import log


def retry(request):
    """Decorator to make get/post requests retryable"""
    @wraps(request)
    def _request_wrapper(*args, **kwargs):
        for i in range(2):
            res = request(*args, **kwargs)
            if res.status_code == 401:
                log('The current API key is invalid or expired.', error=True)
                purge_api_key()

                # This will ensure that fresh api token is requested
                if 'headers' in kwargs:
                    kwargs['headers']['Authorization'] = "Bearer " + get_api_key()
            else:
                return res
        return res

    return _request_wrapper


@retry
def get(url, params=None, **kwargs):
    """Retryable GET request"""
    return requests.get(url, params=params, **kwargs)


@retry
def post(url, data=None, json=None, **kwargs):
    """Retryable POST request"""
    return requests.post(url, data=data, json=json, **kwargs)


def _msg(res):
    try:
        data = res.json()
        if 'errors' in data and len(data['errors']) > 0:
            return data['errors'][0]['message']
        if 'message' in data:
            return data['message']
        if 'msg' in data:
            return data['msg']
    except:
        if res.text:
            return res.text
        return 'Something went wrong'


def pretty(res):
    """Make a human readable output from an HTML response"""
    return '(HTTP ' + str(res.status_code) + ') ' + _msg(res)
