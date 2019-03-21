import argparse
import webbrowser
from jovian.utils.clone import clone, pull
from jovian.utils.install import install, activate
from jovian._version import __version__


def exec_clone(slug):
    clone(slug)


def exec_init():
    from jovian.utils.api import get_api_key
    from jovian.utils.credentials import get_guest_key
    # webbrowser.open('https://jvn.io/')
    get_guest_key()
    get_api_key()
    print('Initialization finished')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('gist', nargs='?')

    args = parser.parse_args()
    command = args.command
    if command == 'init':
        exec_init()
    elif command == 'clone':
        if not args.gist:
            print('Please provide the Gist ID to clone')
            return
        exec_clone(args.gist)
    elif command == 'pull':
        pull(args.gist)
    elif command == 'version':
        print('Jovian library version: ' + __version__)
    elif command == 'install':
        install()
    elif command == 'activate':
        activate()


if __name__ == '__main__':
    main()
