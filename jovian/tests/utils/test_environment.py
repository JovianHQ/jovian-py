import pytest
from unittest import mock, TestCase
from unittest.mock import ANY
import os
from jovian.utils.environment import (get_conda_bin, get_conda_env_name, read_conda_env,
                                      upload_conda_env, print_conda_message, read_pip_env, upload_pip_env)
from jovian.utils.error import CondaError

pip_env = """
alabaster==0.7.12
apipkg==1.5
appdirs==1.4.3
appnope==0.1.0
argh==0.26.2
astroid==2.2.5
attrs==19.1.0
autopep8==1.5
Babel==2.7.0"""


def mock_os_popen(num):
    ret1, ret2 = mock.Mock(), mock.Mock()
    if num == 0:
        ret1.read().strip.return_value = 'usage: conda [-h] [-V] command ...'
        ret2.read().strip.return_value = '/Users/rohitsanjay/miniconda3/bin/conda'
        return ret1, ret2

    elif num == 1:
        ret1.read().strip.return_value = ''
        return ret1, ret1

    elif num == 2:
        ret1.read().strip.return_value = ''
        ret2.read().strip.return_value = '/Users/rohitsanjay/miniconda3/bin/conda'
        return ret1, ret2, ret1

    elif num == 3:
        ret1.read().strip.return_value = 'fake-env'
        return [ret1]

    elif num == 4:
        ret1.read().strip.return_value = ''
        return [ret1]

    elif num == 5:
        ret1.read().strip.return_value = '$CONDA_DEFAULT_ENV'
        return [ret1]

    elif num == 6:
        ret3 = mock.Mock()

        ret1.read().strip.return_value = 'fake-env'  # first call, third call
        ret2.read().strip.return_value = 'conda'  # second call
        ret3.read.return_value = """name: jovian-py-dev
channels:
  - defaults
dependencies:
  - appnope=0.1.0
  - blas=1.0
prefix: /Users/rohitsanjay/miniconda3/envs/jovian-py-dev"""

        return [ret1, ret2, ret1, ret3]

    elif num == 7:
        ret3 = mock.Mock()

        ret1.read().strip.return_value = 'fake-env'  # first call, third call
        ret2.read().strip.return_value = 'conda'  # second call
        ret3.read.return_value = ''

        return [ret1, ret2, ret1, ret3]

    elif num == 8:
        ret1.read.return_value = pip_env
        return [ret1]

    elif num == 9:
        ret1.read.return_value = ''
        return [ret1]


@mock.patch("os.popen", side_effect=mock_os_popen(0))
def test_get_conda_bin(mock_popen):
    assert get_conda_bin() == 'conda'


@mock.patch("os.popen", side_effect=mock_os_popen(1))
def test_get_conda_bin_look_for_conda_exe(mock_popen):
    assert get_conda_bin() == 'conda'


@mock.patch("os.popen", side_effect=mock_os_popen(2))
def test_get_conda_bin_look_for_conda_exe_raises_error(mock_popen):
    with pytest.raises(CondaError):
        get_conda_bin()


@mock.patch("os.popen", side_effect=mock_os_popen(3))
def test_get_conda_env_name(mock_popen):
    assert get_conda_env_name() == 'fake-env'


@mock.patch("os.popen", side_effect=mock_os_popen(4))
def test_get_conda_env_name_base(mock_popen):
    assert get_conda_env_name() == 'base'


@mock.patch("os.popen", side_effect=mock_os_popen(5))
def test_get_conda_env_name_echo_conda_default_env(mock_popen):
    assert get_conda_env_name() == 'base'


@mock.patch("os.popen", side_effect=mock_os_popen(6))
def test_read_conda_env_name_none(mock_popen):
    expected_result = """name: jovian-py-dev
channels:
  - defaults
dependencies:
  - appnope=0.1.0
  - blas=1.0
prefix: /Users/rohitsanjay/miniconda3/envs/jovian-py-dev"""
    assert read_conda_env() == expected_result


@mock.patch("os.popen", side_effect=mock_os_popen(7))
def test_read_conda_env_empty_env_str_raises_error(mock_popen):
    with pytest.raises(CondaError):
        read_conda_env()


@mock.patch("jovian.utils.environment.get_platform", return_value="macos")
@mock.patch("jovian.utils.environment.upload_file")
@mock.patch("os.popen", side_effect=mock_os_popen(6))
def test_upload_conda_env(mock_popen, mock_upload_file, mock_get_platform):
    env_str = """name: jovian-py-dev
channels:
  - defaults
dependencies:
  - appnope=0.1.0
  - blas=1.0
prefix: /Users/rohitsanjay/miniconda3/envs/jovian-py-dev"""
    # setUp - Create pre-existing environment.yml file
    with open('environment-linux.yml', 'w') as f:
        f.write(env_str)

    upload_conda_env('fake_gist_slug', version=2)

    calls = [
        mock.call(
            gist_slug='fake_gist_slug',
            file=('environment.yml', env_str),
            version=2),
        mock.call(
            gist_slug='fake_gist_slug',
            file=('environment-linux.yml', ANY),
            version=2),
        mock.call(
            gist_slug='fake_gist_slug',
            file=('environment-macos.yml', env_str),
            version=2)
    ]
    try:
        mock_upload_file.assert_has_calls(calls)
    finally:
        # tearDown
        os.remove('environment-linux.yml')


def test_print_conda_message(capsys):
    print_conda_message('fake-env')

    expected_result = """[jovian] 
#
# To activate this environment, use
#
#     $ conda activate fake-env
#
# To deactivate an active environment, use
#
#     $ conda deactivate"""
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()


@mock.patch("os.popen", side_effect=mock_os_popen(8))
def test_read_pip_env(mock_popen):
    expected_result = pip_env

    assert read_pip_env() == expected_result


@mock.patch("os.popen", side_effect=mock_os_popen(9))
def test_read_pip_env_raise_error(mock_popen):

    with pytest.raises(Exception):
        read_pip_env()


@mock.patch("jovian.utils.environment.upload_file")
@mock.patch("os.popen", side_effect=mock_os_popen(8))
def test_upload_pip_env(mock_popen, mock_upload_file):
    upload_pip_env('fake_gist_slug', version=2)

    mock_upload_file.assert_called_with(gist_slug='fake_gist_slug', file=('requirements.txt', pip_env), version=2)
