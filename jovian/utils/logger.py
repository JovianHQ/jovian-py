from __future__ import print_function
import click


def log(msg, pre=True, error=False, warn=False, color=None):
    """Print a message to stdout"""
    if error:
        click.secho(('[jovian] ' if pre else '') + 'Error: ' + msg, err=True, fg='red')
    elif warn:
        click.secho(('[jovian] ' if pre else '') + msg, fg='yellow')
    else:
        click.echo(('[jovian] ' if pre else '') + click.style(msg, fg=color))
