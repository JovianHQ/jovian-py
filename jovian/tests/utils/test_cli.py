import pytest
from click.testing import CliRunner
from unittest import mock
from jovian.cli import main


@pytest.fixture(scope='module')
def runner():
    # Get instance of CliRunner
    runner = CliRunner()
    return runner


@mock.patch("jovian.cli.configure")
def test_configure(mock_configure, runner):
    result = runner.invoke(main, ['configure'])
    mock_configure.assert_called_with()
    assert result.exit_code == 0


@mock.patch("jovian.cli.reset_config")
def test_reset(mock_reset, runner):
    result = runner.invoke(main, ['reset'])
    mock_reset.assert_called_with()
    assert result.exit_code == 0


@mock.patch("jovian.cli.activate")
def test_activate(mock_activate, runner):
    result = runner.invoke(main, ['activate'])
    mock_activate.assert_called_with()
    assert result.exit_code == 0


@mock.patch("jovian.cli.add_slack")
def test_add_slack(mock_add_slack, runner):
    result = runner.invoke(main, ['add-slack'])
    mock_add_slack.assert_called_with()
    assert result.exit_code == 0


@mock.patch("jovian.cli.setup_extension")
def test_enable_extension(mock_setup_extension, runner):
    result = runner.invoke(main, ['enable-extension'])
    mock_setup_extension.assert_called_with(enable=True)
    assert result.exit_code == 0


@mock.patch("jovian.cli.setup_extension")
def test_disable_extension(mock_setup_extension, runner):
    result = runner.invoke(main, ['disable-extension'])
    mock_setup_extension.assert_called_with(enable=False)
    assert result.exit_code == 0


@mock.patch("jovian.cli.install")
def test_install(mock_install, runner):
    result = runner.invoke(main, ['install'])
    mock_install.assert_called_with()
    assert result.exit_code == 0


@mock.patch("jovian.cli.install")
def test_install_with_name(mock_install, runner):
    result = runner.invoke(main, ['install', '-n', 'environment-name'])
    mock_install.assert_called_with(env_name='environment-name')
    assert result.exit_code == 0


@mock.patch("jovian.cli.clone")
def test_clone(mock_clone, runner):
    result = runner.invoke(main, ['clone', 'aakashns/jovian-tutorial', '-v', 3])
    mock_clone.assert_called_with(slug='aakashns/jovian-tutorial', version=3, include_outputs=True)
    assert result.exit_code == 0


@mock.patch("jovian.cli.clone")
def test_clone_with_no_outputs(mock_clone, runner):
    result = runner.invoke(main, ['clone', 'aakashns/jovian-tutorial', '-v', 3, '--no-outputs'])
    mock_clone.assert_called_with(slug='aakashns/jovian-tutorial', version=3, include_outputs=False)
    assert result.exit_code == 0


@mock.patch("jovian.cli.pull")
def test_pull(mock_pull, runner):
    result = runner.invoke(main, ['pull', '-n', 'aakashns/jovian-tutorial', '-v', 3])
    mock_pull.assert_called_with(slug='aakashns/jovian-tutorial', version=3)
    assert result.exit_code == 0


@mock.patch("jovian.cli.pull")
def test_pull(mock_pull, runner):
    result = runner.invoke(main, ['pull', '-n', 'aakashns/jovian-tutorial', '-v', 3])
    mock_pull.assert_called_with(slug='aakashns/jovian-tutorial', version=3)
    assert result.exit_code == 0
