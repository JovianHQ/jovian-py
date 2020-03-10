"""Git related utilities"""
import os
import subprocess


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
