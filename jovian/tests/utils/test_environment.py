import pytest
from textwrap import dedent
from unittest import mock, TestCase
from unittest.mock import ANY
import os
from jovian.utils.environment import (get_conda_bin, get_conda_env_name, read_conda_env,
                                      upload_conda_env, print_conda_message, read_pip_env, upload_pip_env)
from jovian.utils.error import CondaError
from jovian.tests.resources.shared import temp_directory

pip_env = dedent("""
            alabaster==0.7.12
            apipkg==1.5
            appdirs==1.4.3
            appnope==0.1.0
            argh==0.26.2
            astroid==2.2.5
            attrs==19.1.0
            autopep8==1.5
            Babel==2.7.0
        """)

ENV_STR = dedent("""
            name: jovian-py-dev
            channels:
            - defaults
            dependencies:
            - appnope=0.1.0
            - blas=1.0
            prefix: /Users/rohitsanjay/miniconda3/envs/jovian-py-dev
        """).strip()


def test_get_conda_bin():
    with mock.patch.dict("os.environ", {"CONDA_EXE": "/Users/username/miniconda3/bin/conda"}, clear=True):
        assert get_conda_bin() == "/Users/username/miniconda3/bin/conda"


@pytest.mark.parametrize(
    "env_dict",
    [
        {"CONDA_EXE": ""},
        {}
    ]
)
def test_get_conda_bin_raises_error(env_dict):
    with mock.patch.dict("os.environ", env_dict, clear=True), pytest.raises(CondaError):
        get_conda_bin()


@pytest.mark.parametrize(
    "env_dict, expected_result",
    [
        ({"CONDA_DEFAULT_ENV": "fake-env"}, "fake-env"),
        ({"CONDA_DEFAULT_ENV": ""}, "base"),
        ({}, "base")
    ]
)
def test_get_conda_env_name(env_dict, expected_result):
    with mock.patch.dict("os.environ", env_dict, clear=True):
        assert get_conda_env_name() == expected_result


@mock.patch("jovian.utils.environment.get_conda_env_name", return_value='fake-env')
@mock.patch("jovian.utils.environment.get_conda_bin", return_value="/usr/bin/conda")
@mock.patch("os.popen")
def test_read_conda_env_name_none(mock_popen, mock_get_conda_bin, mock_get_conda_env_name):
    mock_popen().read.return_value = ENV_STR
    assert read_conda_env() == ENV_STR


@mock.patch("jovian.utils.environment.get_conda_env_name", return_value='no-env')
@mock.patch("jovian.utils.environment.get_conda_bin", return_value="/usr/bin/conda")
@mock.patch("os.popen")
def test_read_conda_env_empty_env_str_raises_error(mock_popen, mock_get_conda_bin, mock_get_conda_env_name):
    mock_popen().read.return_value = ''
    with pytest.raises(CondaError):
        read_conda_env()


@mock.patch("jovian.utils.environment.read_conda_env")
@mock.patch("jovian.utils.environment.get_conda_env_name")
@mock.patch("jovian.utils.environment.get_platform", return_value="macos")
@mock.patch("jovian.utils.environment.upload_file")
def test_upload_conda_env(mock_upload_file, mock_get_platform, mock_get_conda_env_name, mock_read_conda_env):
    with temp_directory():
        mock_read_conda_env.return_value = ENV_STR

        with open('environment-linux.yml', 'w') as f:
            f.write(ENV_STR)

        upload_conda_env('fake_gist_slug', version=2)

        calls = [
            mock.call(
                gist_slug='fake_gist_slug',
                file=('environment.yml', ENV_STR),
                version=2),
            mock.call(
                gist_slug='fake_gist_slug',
                file=('environment-linux.yml', ANY),
                version=2),
            mock.call(
                gist_slug='fake_gist_slug',
                file=('environment-macos.yml', ENV_STR),
                version=2)
        ]

        mock_upload_file.assert_has_calls(calls)


def test_print_conda_message(capsys):
    print_conda_message('fake-env')

    expected_result = dedent("""
                        [jovian] 
                        #
                        # To activate this environment, use
                        #
                        #     $ conda activate fake-env
                        #
                        # To deactivate an active environment, use
                        #
                        #     $ conda deactivate
                    """).strip()
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()


@mock.patch("os.popen")
def test_read_pip_env(mock_popen):
    mock_popen().read.return_value = pip_env
    assert read_pip_env() == pip_env


@mock.patch("os.popen")
def test_read_pip_env_raise_error(mock_popen):
    mock_popen().read.return_value = ''
    with pytest.raises(Exception):
        read_pip_env()


@mock.patch("jovian.utils.environment.upload_file")
@mock.patch("os.popen")
def test_upload_pip_env(mock_popen, mock_upload_file):
    mock_popen().read.return_value = pip_env
    upload_pip_env('fake_gist_slug', version=2)

    mock_upload_file.assert_called_with(gist_slug='fake_gist_slug', file=('requirements.txt', pip_env), version=2)
