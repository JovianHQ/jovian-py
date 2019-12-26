import os
import shutil
from unittest import TestCase, mock

from jovian.utils.git import is_git, get_branch, get_remote, get_repository_root, get_current_commit, commit, git_push, git_commit_push, get_relative_path

path = 'mock_git_repo'


class GitMasterBranch(TestCase):
    path = 'mock_git_repo'
    origin_url = 'https://github.com/rohitsanj/mock_repo.git'

    def setUp(self):
        os.mkdir(self.path)
        os.chdir(self.path)
        os.system("""git init
        mkdir -p ./nested/folder/deep && touch ./nested/folder/deep/sample.ipynb""")
        os.chdir('nested/folder/deep')
        os.system('git add . && git commit -m "initial commit"')

    def tearDown(self):
        os.chdir('../../../../')
        shutil.rmtree(self.path)


class GitSampleBranch(GitMasterBranch):

    def setUp(self):
        super().setUp()
        os.system('git checkout -b sample_branch')


class TempFolder(TestCase):
    sample_folder = '/tmp/sample_folder'
    owd = os.getcwd()

    def setUp(self):
        os.mkdir(self.sample_folder)
        os.chdir(self.sample_folder)

    def tearDown(self):
        shutil.rmtree(self.sample_folder)
        os.chdir(self.owd)


class TestIsGit(GitMasterBranch):

    def test_is_git(self):
        self.assertTrue(is_git())


class TestIsNotGit(TempFolder):

    def test_is_not_git(self):
        self.assertFalse(is_git())


class TestGetBranchMaster(GitMasterBranch):

    def test_get_branch(self):
        expected_result = "master"
        self.assertEqual(get_branch(), expected_result)


class TestGetBranchSample(GitSampleBranch):

    def test_get_branch(self):
        expected_result = "sample_branch"
        self.assertEqual(get_branch(), expected_result)


class TestGetRemote(GitMasterBranch):

    def test_get_remote(self):
        expected_result = ''
        self.assertEqual(get_remote(), expected_result)


class TestGetRemoteNotSet(GitMasterBranch):
    def setUp(self):
        super().setUp()
        os.system('git remote add origin https://github.com/rohitsanj/mock_repo.git')

    def test_get_remote(self):
        expected_result = 'https://github.com/rohitsanj/mock_repo'
        self.assertEqual(get_remote(), expected_result)


class TestGetRepositoryRoot(GitMasterBranch):
    def setUp(self):
        super().setUp()
        os.makedirs('folder1/folder2')
        os.system('cd folder1/folder2')

    def test_get_repository_root(self):
        expected_result = os.path.join(os.path.abspath('../../../'))
        self.assertEqual(get_repository_root(), expected_result)

    def tearDown(self):
        os.system('cd -')
        shutil.rmtree('folder1')
        super().tearDown()


class TestGetCurrentCommit(GitMasterBranch):

    def test_get_current_commit(self):
        expected_result = os.popen('git rev-parse HEAD').read().strip()

        self.assertEqual(get_current_commit(), expected_result)


class TestGetCurrentCommitSample(GitSampleBranch):

    def test_get_current_commit(self):
        expected_result = os.popen('git rev-parse HEAD').read().strip()

        self.assertEqual(get_current_commit(), expected_result)


class TestCommit(GitMasterBranch):
    def setUp(self):
        super().setUp()
        os.system('touch file')

    def test_commit(self):
        message = 'sample commit'
        expected_result = 'cd ' + get_repository_root() + ' && git add . &&  git commit -a -m "sample commit" && cd -'

        self.assertEqual(commit(message), 0)


class TestGitPush(GitMasterBranch):

    @mock.patch("os.system")
    def test_git_push(self, mock_system):
        expected_result = "git push origin master"

        git_push()
        mock_system.assert_called_with(expected_result)


class TestGitPushSample(GitSampleBranch):

    @mock.patch("os.system")
    def test_git_push_sample(self, mock_system):
        expected_result = "git push origin sample_branch"

        git_push()
        mock_system.assert_called_with(expected_result)


class TestGitCommitPush(GitMasterBranch):

    def test_git_commit_push(self):
        message = 'sample commit'
        expected_result = {
            'remote': get_remote(),
            'branch': get_branch(),
            'commit': get_current_commit()
        }

        self.assertEqual(git_commit_push(message), expected_result)


class TestGetRelativePath(GitMasterBranch):

    def test_get_relative_path(self):
        expected_result = "nested/folder/deep"

        self.assertEqual(get_relative_path(), expected_result)
