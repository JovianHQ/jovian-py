from __future__ import print_function
import click


def log(msg, pre=True, error=False, color=None):
    """Print a message to stdout"""
    if error:
        click.secho(('[jovian] ' if pre else '') + 'Error: ' + msg, err=True, fg='bright_red')
    else:
        click.echo(('[jovian] ' if pre else '') + click.style(msg, fg=color))
