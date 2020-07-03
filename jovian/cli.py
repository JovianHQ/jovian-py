import sys

import click

from jovian._version import __version__
from jovian.utils.clone import clone, pull
from jovian.utils.commit import commit_path
from jovian.utils.configure import configure, reset_config
from jovian.utils.extension import setup_extension
from jovian.utils.install import activate, install
from jovian.utils.logger import log
from jovian.utils.misc import is_py2
from jovian.utils.rcfile import set_notebook_slug
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
def help(ctx):  # no-cover
    """Print this help message."""

    # Pretend user typed 'jovian --help' instead of 'jovian help'.
    sys.argv[1] = "--help"
    main()


@main.command('version')
@click.pass_context
def main_version(ctx):  # no-cover
    """Print installed Jovian library version."""

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
@click.option('-n', '--name', 'name', help="Name of conda env")
@click.pass_context
def install_env(ctx, name=None):
    """Install packages from environment file:

        $ jovian install

    or, to specify environment name:

        $ jovian install -n my_env

    """

    if not name:
        install()
    else:
        install(env_name=name)


@main.command("activate")
@click.pass_context
def activate_env(ctx):
    """Activate conda environment from environment file."""

    activate()


@main.command("clone", short_help="Clone a notebook hosted on Jovian")
@click.argument('notebook', metavar="<username/title>")
@click.option('-v', '--version', 'version', help="Version number")
@click.option('--no-outputs', 'no_outputs', is_flag=True, default=False, help="Exclude output files")
@click.option('--overwrite', 'overwrite', is_flag=True, help="Overwrite existing project")
@click.pass_context
def exec_clone(ctx, notebook, version, no_outputs, overwrite):
    """Clone a notebook hosted on Jovian:

        $ jovian clone aakashns/jovian-tutorial

    Or clone a specific version of notebook:

        $ jovian clone aakashns/jovian-tutorial -v 10
    """
    clone(slug=notebook, version=version, include_outputs=not no_outputs, overwrite=overwrite)


@main.command("pull", short_help="Fetch new version of notebook hosted Jovian.")
@click.option('-n', '--notebook', 'notebook', help="Notebook project (format: username/title)")
@click.option('-v', '--version', 'version', help="Version number")
@click.pass_context
def exec_pull(ctx, notebook, version):
    """Fetch the new version of notebook hosted on Jovian(inside a cloned directory):

        $ jovian pull 

    Or fetch a specific version of a specific notebook:

        $ jovian pull -n aakashns/jovian-tutorial -v 10
    """

    pull(slug=notebook, version=version)


@main.command("set-project", short_help="Associate a notebook (filename.ipynb) to a Jovian project (username.title)")
@click.argument('notebook')
@click.argument('project')
@click.pass_context
def set_project(ctx,  notebook, project):
    """Associate notebook (filename.ipynb) to Jovian project (username/title)

        $ jovian set-project my_notebook.ipynb danb/keras-example

    This will create or update the .jovianrc file in the current directory to ensure that commits
    inside the Jupyter notebook "my_notebook.ipynb" add new versions to the project danb/keras-example
    """
    set_notebook_slug(filename=notebook, slug=project)


@main.command("commit", short_help="Create a new notebook on Jovian")
@click.argument('notebook')
@click.pass_context
def exec_commit(ctx, notebook):
    """Create a new notebook on Jovian

        $ jovian commit my_notebook.ipynb
    """
    if is_py2():
        log("Committing is not supported for Python 2.x. Please install and run Jovian from Python 3.5 and above.",
            warn=True)
    commit_path(path=notebook, environment=None, is_cli=True)


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
