import os
from unittest import TestCase, mock

from jovian.utils.git import is_git, get_branch, get_remote, get_repository_root, get_current_commit, commit, git_push, git_commit_push, get_relative_path

path = 'mock_git_repo'


class GitSetup(TestCase):
    path = 'mock_git_repo'
    origin_url = 'https://github.com/rohitsanj/mock_repo.git'

    def setUp(self):
        os.mkdir(self.path)
        os.chdir(self.path)
        os.system("""git init
        git remote add origin {}
        touch sample.txt && git add . && git commit -m "initial commit"
        """.format(self.origin_url))

    def tearDown(self):
        os.chdir('..')
        os.system('rm -rf ' + self.path)


class TestIsGit(GitSetup):

    def test_is_git(self):
        self.assertTrue(is_git())


class TestGetBranch(GitSetup):

    def test_get_branch(self):
        expected_result = "master"
        self.assertEqual(get_branch(), expected_result)


class TestGetRemote(GitSetup):

    def test_get_remote(self):
        expected_result = 'https://github.com/rohitsanj/mock_repo'
        self.assertEqual(get_remote(), expected_result)


class TestGetRepositoryRoot(GitSetup):

    def test_get_repository_root(self):
        expected_result = os.path.join(os.path.abspath('..'), path)
        self.assertEqual(get_repository_root(), expected_result)


class TestGetCurrentCommit(GitSetup):

    def test_get_current_commit(self):
        expected_result = os.popen('git rev-parse HEAD').read().strip()

        self.assertEqual(get_current_commit(), expected_result)


class TestCommit(GitSetup):

    @mock.patch("jovian.utils.git.os")
    def test_commit(self, mock_os):
        message = 'sample commit'
        expected_result = 'cd ' + get_repository_root() + ' && git add . &&  git commit -a -m "' + message + '" && cd -'

        commit(message)
        mock_os.system.assert_called_with(expected_result)


class TestGitPush(GitSetup):

    @mock.patch("jovian.utils.git.os")
    def test_git_push(self, mock_os):
        expected_result = "git push origin " + get_branch()

        git_push()
        mock_os.system.assert_called_with(expected_result)


class TestGitCommitPush(GitSetup):

    @mock.patch("jovian.utils.git.os")
    def test_git_commit_push(self, mock_os):
        message = 'sample commit'
        expected_result = {
            'remote': get_remote(),
            'branch': get_branch(),
            'commit': get_current_commit()
        }

        self.assertEqual(git_commit_push(message), expected_result)


class TestGetRelativePath(GitSetup):

    def test_get_relative_path(self):
        expected_result = "."

        self.assertEqual(get_relative_path(), expected_result)
