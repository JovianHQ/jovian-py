import os
from unittest import TestCase

from jovian.utils.git import is_git

path = 'mock_git_repo'


class GitSetup(TestCase):
    @classmethod
    def setUp(self):
        if not os.path.exists(path):
            os.mkdir(path)
            os.chdir(path)
        os.system('git init')
        os.system('touch sample.txt && git add . && git commit -m "initial commit"')

    @classmethod
    def tearDown(self):
        os.system('cd -')
        os.system('rm -rf ' + path)


class TestIsGit(GitSetup):

    def test_is_git(self):
        self.assertTrue(is_git())
