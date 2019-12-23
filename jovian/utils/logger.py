from __future__ import print_function
import sys


def log(msg, error=False):
    """Print a message to stdout"""
    if error:
        print('[jovian] Error: ' + msg, file=sys.stderr)
    else:
        print('[jovian] ' + msg)
