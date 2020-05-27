import os
import shutil
import textwrap
from unittest import TestCase, mock
from contextlib import contextmanager
from subprocess import check_call
from jovian.tests.resources.shared import temp_directory, mock_git_repo
from jovian.utils.git import (commit, get_branch, get_current_commit, get_relative_path, get_remote,
                              get_repository_root, git_commit_push, git_push, is_git)


def test_is_git():
    with mock_git_repo():
        assert is_git()


def test_is_not_git():
    with temp_directory():
        assert not is_git()


def test_get_branch():
    with mock_git_repo():
        assert get_branch() == "master"

        os.system('git checkout -b sample_branch')
        assert get_branch() == "sample_branch"


def test_get_remote():
    with mock_git_repo():
        expected_result = 'https://github.com/JovianML/mock_repo'
        assert get_remote() == expected_result


def test_get_repository_root():
    with mock_git_repo():
        assert get_repository_root().endswith('mock_git_repo')


def test_get_current_commit():
    with mock_git_repo():
        expected_result = os.popen('git rev-parse HEAD').read().strip()

        assert get_current_commit() == expected_result


def test_commit():
    with mock_git_repo():
        os.system('touch file')
        message = 'sample commit'
        assert commit(message) == 0


@mock.patch("os.system")
def test_git_push_master(mock_system):
    with mock_git_repo():
        git_push()
        mock_system.assert_called_with("git push origin master")


@mock.patch("os.system")
def test_git_push_other_branch(mock_system):
    with mock_git_repo():
        check_call("git checkout -b sample_branch".split())

        git_push()
        mock_system.assert_called_with("git push origin sample_branch")


@mock.patch("jovian.utils.git.git_push")
def test_git_commit_push(mock_git_push):
    with mock_git_repo():
        message = 'sample commit'
        expected_result = {
            'remote': get_remote(),
            'branch': get_branch(),
            'commit': get_current_commit()
        }

        assert git_commit_push(message) == expected_result
        mock_git_push.assert_called_with()


def test_get_relative_path():
    with mock_git_repo():
        os.makedirs("nested/folder/deep")
        os.chdir("nested/folder/deep")

        assert get_relative_path() == "nested/folder/deep"
