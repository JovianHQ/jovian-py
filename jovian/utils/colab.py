import sys

_colab_file_id = None


def in_colab():
    return 'google.colab' in sys.modules


def set_colab_file_id(colab_file_id):
    global _colab_file_id
    _colab_file_id = file_id


def get_colab_file_id():
    global _colab_file_id
    return _colab_file_id
