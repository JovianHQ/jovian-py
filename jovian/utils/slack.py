from jovian._version import __version__
from jovian.utils.credentials import get_api_key, get_guest_key, read_api_url, read_org_id
from jovian.utils.error import ApiError
from jovian.utils.logger import log
from jovian.utils.request import get, pretty
from jovian.utils.shared import _u, _v
from jovian.utils.api import post_slack_message


def _h():
    """Create a header to provide library metadata"""
    return {"Authorization": "Bearer " + get_api_key(),
            "x-jovian-source": "library",
            "x-jovian-library-version": __version__,
            "x-jovian-command": "add-slack",
            "x-jovian-guest": get_guest_key(),
            "x-jovian-org": read_org_id()}


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


def notify(data, verbose=True, safe=False):
    """Sends the data to the `Slack`_ workspace connected with your `Jovian`_ account.

    Args:
        data(dict|string): A dict or string to be pushed to Slack

        verbose(bool, optional): By default it prints the acknowledgement, you can remove this by setting the argument to False.

        safe(bool, optional): To avoid raising ApiError exception. Defaults to False.

    Example
        .. code-block::

            import jovian

            data = "Hello from the Integration!"
            jovian.notify(data)

    .. important::
        This feature requires for your Jovian account to be connected to a Slack workspace, visit `Jovian Integrations`_ to integrate them and to control the type of notifications.
    .. _Slack: https://slack.com
    .. _Jovian: https://jovian.ai?utm_source=docs
    .. _Jovian Integrations: https://jovian.ai/settings/integrations?utm_source=docs
    """
    res = post_slack_message(data=data, safe=safe)
    if verbose:
        if not res.get('errors'):
            log('message_sent:' + str(res.get('data').get('messageSent')))
        else:
            log(str(res.get('errors')[0].get('message')), error=True)
