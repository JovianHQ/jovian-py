"""Git related utilities"""
import os
import subprocess
from urllib.parse import urlparse

from jovian.utils.credentials import get_api_key, read_api_url

HOME = os.path.expanduser('~')


def is_git():
    """Check whether we are in a git repository"""
    task = subprocess.Popen('git rev-parse', shell=True, stderr=subprocess.PIPE)
    task.communicate()
    return task.returncode == 0


def get_branch():
    return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()


def get_remote():
    """Get the remote URL"""
    return os.popen('git config --get remote.origin.url').read().replace(".git\n", "").strip()


def get_current_commit():
    """Get the current commit"""
    return os.popen('git rev-parse HEAD').read().strip()


def get_repository_root():
    """Get the root of the git repository"""
    return os.popen('git rev-parse --show-toplevel').read().strip()


def commit(message):
    """Create a new commit"""
    return os.system('cd ' + get_repository_root() + ' && git add . &&  git commit -a -m "' + message + '" && cd -')


def git_push():
    """Push the branch to origin"""
    return os.system("git push origin " + get_branch())


def remote_update():
    """Updates all the remotes"""
    return os.system("git remote update") == 0


def is_up_to_date():
    return "behind" not in os.popen("git status -uno").read().splitlines()[1]


def is_jovian_remote(remote):
    return urlparse(read_api_url()).netloc == urlparse(remote).netloc


def insert_git_credential(username):
    api_url = urlparse(read_api_url())
    password = get_api_key()
    git_creds_path = fetch_git_credential_path(username)
    with open(git_creds_path, 'w') as f:
        f.write(construct_git_creds(api_url, username, password))

    return os.system("git config credential.helper 'store --file {}'".format(git_creds_path))


def construct_git_creds(api_url, username, password):
    return api_url.scheme + "://" + username + ":" + password + "@" + api_url.netloc + "\n"


def fetch_git_credential_path(username):
    return os.path.join(HOME, '.git-jovian-credentials-{}'.format(username))


def check_write_access():
    return os.system("git push origin " + get_branch() + " --dry-run") == 0


def is_index_dirty():
    return os.popen('git status --porcelain').read().strip() != ""


def git_commit_push(message):
    """Create a commit and push to origin"""
    if is_git():
        commit(message)
        git_push()
        return {
            'remote': get_remote(),
            'branch': get_branch(),
            'commit': get_current_commit()
        }


def get_relative_path():
    """Returns relative path from the git root directory."""
    root_dir = get_repository_root()
    file_dir = os.path.abspath('')
    return os.path.relpath(file_dir, root_dir)
