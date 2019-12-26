import sys

import click

from jovian._version import __version__
from jovian.utils.clone import clone, pull
from jovian.utils.configure import configure, reset_config
from jovian.utils.extension import setup_extension
from jovian.utils.install import activate, install
from jovian.utils.slack import add_slack


@click.group()
@click.version_option(version=__version__, prog_name="Jovian")
@click.pass_context
def main(ctx, log_level="info"):
    """Keep track of your Jupyter notebooks using Jovian.

    Use within your Jupyter notebooks:

        [1] import jovian

        [2] jovian.commit()

    Or try out a demo with:

        $ jovian clone aakashns/jovian-tutorial
    """

    pass


@main.command("help")
@click.pass_context
def help(ctx):
    """Print this help message."""

    # Pretend user typed 'jovian --help' instead of 'jovian help'.
    sys.argv[1] = "--help"
    main()


@main.command('version')
@click.pass_context
def main_version(ctx):
    """Print Jovian’s version number."""

    # Pretend user typed 'jovian --version' instead of 'jovian version'
    sys.argv[1] = "--version"
    main()


@main.command("configure")
@click.pass_context
def create_config(ctx):
    """Configure Jovian for Pro users."""

    configure()


@main.command("reset")
@click.pass_context
def reset(ctx):
    """Reset Jovian config."""
    reset_config()


@main.command("install", short_help="Install packages from environment file.")
@click.option('-n', '--name', 'name')
@click.pass_context
def install_env(ctx, name=None):
    """Install packages from environment file:

        $ jovian install

    or, install from specific environment file

        $ jovian install environment-linux.yml
    """

    if not name:
        install()
    elif name:
        install(env_name=name)
    else:
        # Show help
        sys.argv[1] = "--help"
        install_env()


@main.command("activate")
@click.pass_context
def activate_env(ctx):
    """Activate conda environment from environment file."""

    activate()


@main.command("clone", short_help="Clone a notebook hosted on Jovian")
@click.argument('notebook')
@click.option('-v', '--version', 'version')
@click.option('--no-outputs', 'no_outputs')
@click.pass_context
def exec_clone(ctx, notebook, version, no_outputs):
    """Clone a notebook hosted on Jovian:

        $ jovian clone aakashns/jovian-tutorial

    Or clone a specific version of notebook:

        $ jovian clone aakashns/jovian-tutorial -v 10
    """

    clone(notebook, version, not no_outputs)


@main.command("pull", short_help="Fetch new version of notebook hosted Jovian.")
@click.option('-n', '--notebook', 'notebook')
@click.option('-v', '--version', 'version')
@click.pass_context
def exec_pull(ctx, notebook, version):
    """Fetch the new version of notebook hosted on Jovian(inside a cloned directory):

        $ jovian pull 

    Or fetch a specific version of a specific notebook:
    (Provide the notebook-name with the username separated by a forward slash)

        $ jovian pull -n aakashns/jovian-tutorial -v 10
    """

    pull(notebook, version)


@main.command("add-slack")
@click.pass_context
def exec_add_slack(ctx):
    """Connect slack to get updates."""

    add_slack()


@main.command("enable-extension")
@click.pass_context
def extension_enable(ctx):
    """Enable Jovian’s Jupyter notebook extension."""

    setup_extension(enable=True)


@main.command("disable-extension")
@click.pass_context
def extension_disable(ctx):
    """Disable Jovian’s Jupyter notebook extension."""

    setup_extension(enable=False)


if __name__ == '__main__':
    main()
