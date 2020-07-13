import sys
from jovian.utils.api import _h, get_current_user
from jovian.utils.error import ApiError
from jovian.utils.logger import log
from jovian.utils.request import post
from jovian.utils.shared import _u
from jovian.utils.request import pretty


_colab_file_id = None


def in_colab():
    return 'google.colab' in sys.modules


def set_colab_file_id(colab_file_id):
    global _colab_file_id
    _colab_file_id = colab_file_id


def get_colab_file_id():
    global _colab_file_id
    return _colab_file_id


def perform_colab_commit(project, privacy):
    # file_id, project, privacy api key
    file_id = get_colab_file_id()
    if file_id is None:
        log("Colab File Id is not provided", error=True)

    # /gist/colab-commit data = {file_id, project}, return status
    if '/' not in project:
        project = get_current_user()['username'] + '/' + project

    data = {'project': project, 'file_id': file_id, 'visibility': privacy}

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
        return res.json()['data']
    raise ApiError('Colab commit failed: ' + pretty(res))
