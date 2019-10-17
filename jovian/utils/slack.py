from jovian._version import __version__
from jovian.utils.credentials import get_api_key, get_guest_key, read_api_url, read_org_id
from jovian.utils.error import ApiError
from jovian.utils.logger import log
from jovian.utils.request import get, pretty
from jovian.utils.url import urljoin


def _u(path):
    """Make a URL from the path"""
    return urljoin(read_api_url(), path)


def _h():
    """Create a header to provide library metadata"""
    return {"Authorization": "Bearer " + get_api_key(),
            "x-jovian-source": "library",
            "x-jovian-library-version": __version__,
            "x-jovian-command": "add-slack",
            "x-jovian-guest": get_guest_key(),
            "x-jovian-org": read_org_id()}


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
        raise ApiError('Slack trigger failed: ' + pretty(res))
