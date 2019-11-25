"""Git related utilities"""
import os
from subprocess import call


def is_git():
    """Check whether we are in a git repository"""
    return call(['git', 'rev-parse']) == 0


def git_branch():
    return os.popen('git branch | grep \* | cut -d \' \' -f2').read().strip()


def git_remote():
    """Get the remote URL"""
    return os.popen('git config --get remote.origin.url').read().replace(".git\n", "").strip()


def git_current_commit():
    """Get the current commit"""
    return os.popen('git rev-parse HEAD').read().strip()


def git_root():
    """Get the root of the git repository"""
    return os.popen('git rev-parse --show-toplevel').read().strip()


def git_commit(message):
    """Create a new commit"""
    return os.system('cd ' + git_root() + ' && git add . &&  git commit -a -m "' + message + '" && cd -')


def git_push():
    """Push the branch to origin"""
    return os.system("git push origin " + git_branch())


def git_commit_push(message):
    """Create a commit and push to origin"""
    if is_git():
        git_commit(message)
        git_push()
        return {
            'remote': git_remote(),
            'branch': git_branch(),
            'commit': git_commit(message)
        }


def git_rel_path():
    """Returns relative path from the git root directory."""
    root_dir = git_root()
    file_dir = os.path.abspath('')
    return os.path.relpath(file_dir, root_dir)
