import sys

from jovian.utils.api import get_current_user, _h, parse_success_response
from jovian.utils.error import ApiError
from jovian.utils.logger import log
from jovian.utils.request import post, pretty
from jovian.utils.shared import _u


_colab_file_id = None


def in_colab():
    return 'google.colab' in sys.modules


def set_colab_file_id(file_id):
    global _colab_file_id
    _colab_file_id = file_id


def get_colab_file_id():
    global _colab_file_id
    return _colab_file_id


def perform_colab_commit(project, privacy):
    if '/' not in project:
        project = get_current_user()['username'] + '/' + project

    data = {'project': project, 'file_id': get_colab_file_id(), 'visibility': privacy}

    if privacy == 'auto':
        data['public'] = True
    elif privacy == 'secret' or privacy == 'private':
        data['public'] = False

    auth_headers = _h()

    log("Uploading colab notebook to Jovian...")
    res = post(url=_u('/gist/colab-commit'),
               data=data,
               headers=auth_headers)

    if res.status_code == 200:
        data, warning = parse_success_response(res)
        if warning:
            log(warning, error=True)
        return data
    raise ApiError('Colab commit failed: ' + pretty(res))
