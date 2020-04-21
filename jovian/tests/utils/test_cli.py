import pytest
from click.testing import CliRunner
from unittest import mock
from jovian.cli import main


@pytest.fixture(scope='module')
def runner():
    # Get instance of CliRunner
    runner = CliRunner()
    return runner


@pytest.mark.parametrize(
    "func, cli_args, called_with_args",
    [
        # enable-extension
        ("setup_extension", ["enable-extension"], {"enable": True}),

        # disable-extension
        ("setup_extension", ["disable-extension"], {"enable": False}),

        # add-slack
        ("add_slack", ["add-slack"], {}),

        # activate
        ("activate", ["activate"], {}),

        # reset
        ("reset_config", ["reset"], {}),

        # configure
        ("configure", ["configure"], {}),

        # install
        ("install", ["install"], {}),
        ("install", ['install', '-n', 'environment-name'], {"env_name": 'environment-name'}),
        ("install", ['install', '--name', 'environment-name'], {"env_name": 'environment-name'}),

        # clone
        (
            "clone",
            ['clone', 'aakashns/jovian-tutorial'],
            {"slug": 'aakashns/jovian-tutorial', "version": None, "include_outputs": True, "overwrite": False}
        ),
        (
            "clone",
            ['clone', 'aakashns/jovian-tutorial', '-v', 3],
            {"slug": 'aakashns/jovian-tutorial', "version": 3, "include_outputs": True, "overwrite": False}
        ),
        (
            "clone",
            ['clone', 'aakashns/jovian-tutorial', '--version', 3],
            {"slug": 'aakashns/jovian-tutorial', "version": 3, "include_outputs": True, "overwrite": False}
        ),
        (
            "clone",
            ['clone', 'aakashns/jovian-tutorial', '-v', 3, '--no-outputs'],
            {"slug": 'aakashns/jovian-tutorial', "version": 3, "include_outputs": False, "overwrite": False}
        ),
        (
            "clone",
            ['clone', 'aakashns/jovian-tutorial', '-v', 3, '--overwrite'],
            {"slug": 'aakashns/jovian-tutorial', "version": 3, "include_outputs": True, "overwrite": True}
        ),

        # pull
        (
            "pull",
            ['pull'],
            {"slug": None, "version": None},
        ),
        (
            "pull",
            ['pull', '-n', 'aakashns/jovian-tutorial'],
            {"slug": 'aakashns/jovian-tutorial', "version": None},
        ),
        (
            "pull",
            ['pull', '-n', 'aakashns/jovian-tutorial', '-v', 3],
            {"slug": 'aakashns/jovian-tutorial', "version": 3},
        ),

        # set-project
        (
            "set_notebook_slug",
            ["set-project", "my_notebook.ipynb", "danb/keras-example"],
            {"filename": "my_notebook.ipynb", "slug": "danb/keras-example"}
        ),
    ]
)
def test_cli(func, cli_args, called_with_args, runner):
    with mock.patch("jovian.cli.{}".format(func)) as mock_func:
        result = runner.invoke(main, cli_args)
        mock_func.assert_called_with(**called_with_args)
        assert result.exit_code == 0
