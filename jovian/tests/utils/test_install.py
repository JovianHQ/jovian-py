import os
from textwrap import dedent
from unittest import TestCase, mock
from unittest.mock import ANY, call
from contextlib import contextmanager

import pytest


from jovian.utils.install import run_command, install, activate
from jovian.tests.resources.shared import temp_directory, fake_envfile


@pytest.mark.parametrize(
    "side_effect, calls",
    [
        (
            [(None, b'')],
            [
                call('conda env update --file environment.yml --name environment-name', shell=True, stderr=ANY),
                call().communicate()
            ]
        ),
        (
            [(None, b"""ResolvePackageNotFound: \n- mixpanel=1.11.0"""), (None, b'')],
            [
                call('conda env update --file environment.yml --name environment-name', shell=True, stderr=ANY),
                call().communicate(),
                call('conda env update --file environment.yml --name environment-name', shell=True, stderr=-1),
                call().communicate(),
            ]
        ),
        (
            [(None, b"""ResolvePackageNotFound: \n- mixpanel=1.11.0"""),
             (None, b"""ResolvePackageNotFound: \n- mixpanel=1.11.0"""),
             (None, b"""ResolvePackageNotFound: \n- mixpanel=1.11.0""")],
            [
                call('conda env update --file environment.yml --name environment-name', shell=True, stderr=ANY),
                call().communicate(),
                call('conda env update --file environment.yml --name environment-name', shell=True, stderr=ANY),
                call().communicate(),
                call('conda env update --file environment.yml --name environment-name', shell=True, stderr=ANY),
                call().communicate()
            ]
        ),
        (
            [(None, b"""Pip failed""")],
            [
                call('conda env update --file environment.yml --name environment-name', shell=True, stderr=ANY),
                call().communicate()
            ]
        ),
    ]
)
@mock.patch("subprocess.Popen")
def test_run_command(mock_popen, side_effect, calls):
    with fake_envfile():
        mock_popen().communicate.side_effect = side_effect
        run_command('conda env update --file environment.yml --name environment-name',
                    'environment.yml', ['mixpanel=1.11.0', 'sigmasix=1.91.0'])

        mock_popen.assert_has_calls(calls)


@mock.patch("jovian.utils.install.get_conda_bin", return_value="conda")
@mock.patch("jovian.utils.install.request_env_name", return_value="test-env")
@mock.patch("jovian.utils.install.run_command")
def test_install(mock_run_command, mock_request_env_name, mock_get_conda_bin):
    with fake_envfile():
        mock_run_command.return_value = True

        install('environment.yml')

        mock_run_command.assert_called_with(
            command='conda env update --file "environment.yml" --name "test-env"',
            env_fname='environment.yml',
            packages=['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite', 'six==1.11.0', 'sqlite==2.0.0'],
            run=1)


@mock.patch("jovian.utils.install.get_conda_bin", return_value="conda")
@mock.patch("jovian.utils.install.identify_env_file", return_value=None)
def test_install_env_fname_none(mock_identify_env_file, mock_get_conda_bin, capsys):
    install()

    expected_result = "[jovian] Error: Failed to detect a conda environment YML file. Skipping.."
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result


@mock.patch("jovian.utils.install.get_conda_bin", return_value="conda")
@mock.patch("jovian.utils.install.request_env_name", return_value=None)
def test_install_env_name_none(mock_request_env_name, mock_get_conda_bin, capsys):
    with fake_envfile():
        install('environment.yml')

        expected_result = dedent("""
            [jovian] Detected conda environment file: environment.yml

            [jovian] Environment name not provided/detected. Skipping..
            """).strip()
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.install.get_conda_bin", return_value="conda")
@mock.patch("jovian.utils.install.request_env_name", return_value="test-env")
@mock.patch("jovian.utils.install.run_command")
def test_install_unsuccessful(mock_run_command, mock_request_env_name, mock_get_conda_bin, capsys):
    with fake_envfile():
        mock_run_command.return_value = False

        install('environment.yml')

        expected_result = dedent("""
                            [jovian] Detected conda environment file: environment.yml

                            [jovian] Some pip packages failed to install.
                            [jovian] 
                            #
                            # To activate this environment, use
                            #
                            #     $ conda activate test-env
                            #
                            # To deactivate an active environment, use
                            #
                            #     $ conda deactivate
                        """).strip()

        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.install.get_conda_bin", return_value="conda")
def test_activate(mock_get_conda_bin, capsys):
    with fake_envfile():
        activate('environment.yml')

        expected_result = dedent("""
            [jovian] Detected conda environment file: environment.yml

            [jovian] Copy and execute the following command (try "source activate" if "conda activate doesn't work" )
                conda activate test-env
        """).strip()

        captured = capsys.readouterr()
        assert expected_result.strip() in captured.out.strip()


def error_raiser(*args, **kwargs):
    raise Exception('fake error')


@mock.patch("jovian.utils.install.get_conda_bin", side_effect=error_raiser)
def test_activate_conda_not_found(mock_get_conda_bin, capsys):
    with fake_envfile():
        assert activate('environment.yml') == False

        expected_result = """[jovian] Error: Anaconda binary not found. Please make sure the "conda" command is in your system PATH or the environment variable $CONDA_EXE points to the anaconda binary"""

        captured = capsys.readouterr()
        assert expected_result.strip() in captured.err.strip()


@mock.patch("jovian.utils.install.identify_env_file", return_value=None)
@mock.patch("jovian.utils.install.get_conda_bin", return_value="conda")
def test_activate_env_fname_none(mock_get_conda_bin, mock_identify_env_file, capsys):
    with fake_envfile():
        assert activate('environment.yml') == False

        expected_result = """[jovian] Error: Failed to detect a conda environment YML file. Skipping.."""

        captured = capsys.readouterr()
        assert expected_result.strip() in captured.err.strip()


@mock.patch("jovian.utils.install.extract_env_name", return_value=None)
@mock.patch("jovian.utils.install.get_conda_bin", return_value="conda")
def test_activate_env_name_none(mock_get_conda_bin, mock_extract_env_name, capsys):
    with fake_envfile():
        activate('environment.yml')

        expected_result = """[jovian] Environment name not provided/detected. Skipping.."""

        captured = capsys.readouterr()
        assert expected_result.strip() in captured.out.strip()
