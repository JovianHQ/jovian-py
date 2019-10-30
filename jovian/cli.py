import argparse
import os
import sys

import click

from jovian._version import __version__
from jovian.utils.clone import clone, pull
from jovian.utils.configure import configure, reset
from jovian.utils.install import activate, install
from jovian.utils.slack import add_slack


def nb_ext(enable=True):
    if enable:
        os.system("jupyter nbextension enable jovian_nb_ext/main --sys-prefix")
    else:
        os.system("jupyter nbextension disable jovian_nb_ext/main --sys-prefix")


@click.group()
@click.version_option(version=__version__, prog_name="Jovian")
@click.pass_context
def main(ctx, log_level="info"):
    """Try out a demo with:

        $ jovian clone aakashns/jovian-tutorial

    Or use within your Jupyter notebook:

        [1] import jovian

        [2] jovian.commit()
    """

    pass


@main.command("help")
@click.pass_context
def help(ctx):
    """Print this help message."""

    # Pretend user typed 'jovian --help' instead of 'jovian help'.
    sys.argv[1] = "--help"
    main()


@main.group('version', invoke_without_command=True)
@click.pass_context
def main_version(ctx):
    """Print Jovian's version number."""

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
def reset_config(ctx):
    """Reset Jovian config."""

    reset()


@main.command("install")
@click.argument('name_argv', nargs=-1)
@click.pass_context
def install_env(ctx, name_argv):
    """Install packages from environment file."""

    if len(name_argv) > 1:
        print("usage")
        return

    name = name_argv[0] if len(name_argv) == 1 else None
    install(env_name=name)


@main.command("activate")
@click.argument('name_argv', nargs=-1)
@click.pass_context
def activate_env(ctx, name_argv):
    """Activate conda environment from environment file."""

    if len(name_argv) > 1:
        click.echo("usage:")
        return

    name = name_argv[0] if len(name_argv) == 1 else None
    activate()


@main.command("clone", short_help="Clone a notebook hosted on Jovian")
@click.argument('notebook')
@click.option('-v', '--version', 'version')
@click.pass_context
def exec_clone(ctx, notebook, version):
    """Clone a notebook hosted on Jovian:

        $ jovian clone aakashns/jovian-tutorial

    Or clone a specific version of notebook:

        $ jovian clone aakashns/jovian-tutorial -v 10
    """

    clone(notebook, version)


@main.command("pull", short_help="Fetch a notebook hosted on Jovian(into current directory).")
@click.argument('notebook')
@click.option('-v', '--version', 'version')
@click.pass_context
def exec_pull(ctx, notebook, version):
    """Fetch a notebook hosted on Jovian(into current directory):

        $ jovian pull aakashns/jovian-tutorial

    Or fetch a specific version of notebook:

        $ jovian pull aakashns/jovian-tutorial -v 10
    """

    pull(notebook, version)


@main.command("add-slack")
@click.pass_context
def exec_add_slack(ctx):
    """Connect slack to get updates."""

    add_slack()


@main.group("extension", invoke_without_command=False)
@click.pass_context
def extension(ctx):
    """Enable/Disable Jovian's Jupyter notebook extension."""
    pass


@extension.command("enable")
def extension_enable():
    """Enable Jovian's Jupyter notebook extension."""

    nb_ext(enable=True)


@extension.command("disable")
def disable_enable():
    """Disable Jovian's Jupyter notebook extension."""

    nb_ext(enable=False)


if __name__ == '__main__':
    main()
