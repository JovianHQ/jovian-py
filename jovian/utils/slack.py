import os
from requests import get
from jovian.utils.credentials import get_guest_key, read_api_key_opt, read_api_url
from jovian.utils.logger import log
from jovian._version import __version__


class ApiError(Exception):
    """Error class for web API related Exceptions"""
    pass


def _u(path):
    """Make a URL from the path"""
    return API_URL + path


def _msg(res):
    try:
        data = res.json()
        if 'errors' in data and len(data['errors'] > 0):
            return data['errors'][0]['message']
        if 'message' in data:
            return data['message']
        if 'msg' in data:
            return data['msg']
    except:
        if res.text:
            return res.text
        return 'Something went wrong'


def _pretty(res):
    """Make a human readable output from an HTML response"""
    return '(HTTP ' + str(res.status_code) + ') ' + _msg(res)


def _h():
    """Create a header to provide library metadata"""
    api_key, _ = read_api_key_opt()

    headers = {"x-jovian-source": "library",
               "x-jovian-library-version": __version__,
               "x-jovian-command": "add-slack",
               "x-jovian-guest": get_guest_key()}

    if api_key is not None:
        headers["Authorization"] = "Bearer " + api_key

    return headers


def _v(version):
    """Create version query parameter string"""
    if version is not None:
        return "?gist_version=" + str(version)
    return ""


def add_slack():
    """prints instructions for connecting Slack, if Slack connection is not already present.
    if Slack is already connected, prints details about the workspace and the channel"""
    url = _u('/slack/integration_details')
    res = get(url, headers=_h())
    if res.status_code == 200:
        res = res.json()
        if not res.get('errors'):
            slack_account = res.get('data').get('slackAccount')
            log('Slack already connected. \nWorkspace: {}\nConnected Channel: {}'
                .format(slack_account.get('workspace'), slack_account.get('channel')))
        else:
            log(str(res.get('errors')[0].get('message')))
    else:
        raise ApiError('Slack trigger failed: ' + _pretty(res))
