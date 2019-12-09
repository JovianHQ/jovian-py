from __future__ import print_function
from sys import stderr
import click


def log(msg, error=False, color=None):
    """Print a message to stdout"""
    if error:
        click.secho('[jovian] Error: ' + msg, err=True, fg='bright_red')
    else:
        click.secho('[jovian] ', bold=True, nl=False)
        click.secho(msg, fg=color)
