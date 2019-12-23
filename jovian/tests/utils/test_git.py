import os
from unittest import TestCase

from jovian.utils.git import is_git, get_branch, get_remote, get_repository_root

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
