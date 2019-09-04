import argparse
import os

from jovian.utils.clone import clone, pull
from jovian.utils.install import install, activate
from jovian.utils.configure import configure, reset
from jovian.utils.slack import add_slack
from jovian.utils.misc import get_flavor
from jovian._version import __version__


def exec_clone(slug, version):
    clone(slug, version)


def nb_ext(enable=True):
    if enable:
        os.system("jupyter nbextension enable jovian_nb_ext/main --sys-prefix")
    else:
        os.system("jupyter nbextension disable jovian_nb_ext/main --sys-prefix")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command')
    parser.add_argument('gist', nargs='?')
    parser.add_argument('-n', '--name')
    parser.add_argument('-v', '--version')

    args = parser.parse_args()
    command = args.command
    if command == 'configure':
        configure()
    if command == 'reset':
        reset()
    elif command == 'clone':
        if not args.gist:
            print('Please provide the Gist ID to clone')
            return
        exec_clone(args.gist, args.version)
    elif command == 'pull':
        pull(args.gist, args.version)
    elif command == 'version':
        print('Jovian library version: ' +
              __version__ + ' (' + get_flavor() + ')')
    elif command == 'install':
        install(env_name=args.name)
    elif command == 'activate':
        activate()
    elif command == 'enable-extension':
        nb_ext()
    elif command == 'disable-extension':
        nb_ext(enable=False)
    elif command == 'add-slack':
        add_slack()


if __name__ == '__main__':
    main()
