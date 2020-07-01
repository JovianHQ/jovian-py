import sys

_colab_file_id = None


def in_colab():
    return 'google.colab' in sys.modules


def set_colab_file_id(colab_file_id):
    global _colab_file_id
    _colab_file_id = colab_file_id


def get_colab_file_id():
    global _colab_file_id
    return _colab_file_id


def perform_colab_commiy():
    # file_id, project, privacy api key

    # /gist/colab-commit data = {file_id, project}, return status

    # return the url
