import argparse
import webbrowser
from jovian.utils.credentials import purge_config
from jovian.utils.clone import clone, pull
from jovian.utils.install import install
from jovian._version import __version__


def exec_clone(slug):
    clone(slug)


def exec_init():
    from jovian.utils.api import get_key
    print('[jovian] Visit https://jvn.io/ to sign up and generate an API key.')
    # webbrowser.open('https://jvn.io/')
    purge_config()
    get_key()
    print('Credentials validated and saved to ~/.jovian/credentials.json.')


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


if __name__ == '__main__':
    main()
