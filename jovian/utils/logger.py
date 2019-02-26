from __future__ import print_function
from sys import stderr


def log(msg, error=False):
    """Print a message to stdout"""
    if error:
        print('[jovian] Error: ' + msg, file=stderr)
    else:
        print('[jovian] ' + msg)
