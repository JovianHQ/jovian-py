import functools
import os
import shutil
from contextlib import contextmanager
from textwrap import dedent
from unittest import mock
from unittest.mock import ANY, call

import pytest

from jovian.tests.resources.shared import fake_creds, fake_records, mock_git_repo, temp_directory, touch
from jovian.utils.commit import (_attach_file, _attach_files, _attach_records, _capture_environment, _list_ipynb_files,
                                 _parse_filename, _parse_project, _perform_git_commit, commit, commit_path)
from jovian.utils.error import CondaError


def mock_get_gist(project):
    responses = {
        "f67108fc906341d8b15209ce88ebc3d2": {
            "slug": "f67108fc906341d8b15209ce88ebc3d2",
            "title": "demo-notebook",
            "owner": {
                "avatar": "https://api-staging.jovian.ai/api/user/rohit/avatar",
                "id": 47,
                "name": "Rohit Sanjay",
                "username": "rohit"
            }
        },
        "rohit/time-series": {
            "slug": "f67108fc906341d8b15209ce88ebc3d2",
            "title": "demo-notebook",
            "owner": {
                "avatar": "https://api-staging.jovian.ai/api/user/rohit/avatar",
                "id": 47,
                "name": "Rohit Sanjay",
                "username": "rohit"
            }
        },
        "rohit/time-series-new":  {
            "slug": None,
            "title": "demo-notebook",
            "owner": {
                "avatar": "https://api-staging.jovian.ai/api/user/rohit/avatar",
                "id": 47,
                "name": "Rohit Sanjay",
                "username": "rohit"
            },
        }
    }

    return responses[project]


@pytest.mark.parametrize(
    "filename, expected_result",
    [
        (None, 'fake-script.py'),
        ('script.py', 'script.py'),
        ('script', 'script.py')
    ]
)
@mock.patch("jovian.utils.commit.get_script_filename", return_value='fake-script.py')
@mock.patch("jovian.utils.commit.in_script", return_value=True)
def test_parse_filename_in_script(mock_in_script, mock_get_script_filename, filename, expected_result):
    assert _parse_filename(filename=filename) == expected_result


@pytest.mark.parametrize(
    "filename, expected_result",
    [
        (None, 'fake-notebook.ipynb'),
        ('notebook.ipynb', 'notebook.ipynb'),
        ('notebook', 'notebook.ipynb')
    ]
)
@mock.patch("jovian.utils.commit.in_script", return_value=False)
@mock.patch("jovian.utils.commit.get_notebook_name", return_value='fake-notebook.ipynb')
@mock.patch("jovian.utils.commit.in_notebook", return_value=True)
def test_parse_filename_in_notebook(mock_in_notebook, mock_get_script_name, mock_in_script, filename, expected_result):
    assert _parse_filename(filename=filename) == expected_result


@pytest.mark.parametrize(
    "get_gist_side_effect, get_gist_access_return_value, args, expected_result",
    [
        (
            mock_get_gist,
            {"write": True},
            {
                "project": None,
                "filename": "file.ipynb",
                "new_project": False,
            },
            ("demo-notebook", "f67108fc906341d8b15209ce88ebc3d2")
        ),
        (
            mock_get_gist,
            {"write": True},
            {
                "project": "rohit/time-series",
                "filename": "file.ipynb",
                "new_project": False,
            },
            ("demo-notebook", "f67108fc906341d8b15209ce88ebc3d2")
        ),
        (
            mock_get_gist,
            {"write": True},
            {
                "project": "time-series",
                "filename": "file.ipynb",
                "new_project": True,
            },
            ("demo-notebook", "f67108fc906341d8b15209ce88ebc3d2")
        ),
        (
            [None],
            {"write": False},
            {
                "project": "time-series",
                "filename": "file.ipynb",
                "new_project": True,
            },
            ("time-series", None)
        ),
        (
            mock_get_gist,
            {"write": False},
            {
                "project": "time-series",
                "filename": "file.ipynb",
                "new_project": True,
            },
            ("demo-notebook", None)
        ),
        (
            mock_get_gist,
            {"write": False},
            {
                "project": "rohit/time-series-new",
                "filename": "file.ipynb",
                "new_project": True,
            },
            ("demo-notebook", None)
        ),
        (
            None,
            None,
            {
                "project": None,
                "filename": "file.ipynb",
                "new_project": True,
            },
            (None, None)
        ),

    ]
)
@mock.patch("jovian.utils.rcfile._current_slug", "f67108fc906341d8b15209ce88ebc3d2")
@mock.patch("jovian.utils.commit.api.get_current_user", return_value={'username': 'rohit'})
def test_parse_project(
        mock_get_current_user, get_gist_side_effect, get_gist_access_return_value, args, expected_result):
    with mock.patch("jovian.utils.commit.api.get_gist", side_effect=get_gist_side_effect), \
            mock.patch("jovian.utils.commit.api.get_gist_access", return_value=get_gist_access_return_value):
        with fake_creds():
            assert _parse_project(**args) == expected_result


@mock.patch("jovian.utils.rcfile._current_slug", None)
@mock.patch("jovian.utils.commit.get_notebook_slug", return_value="rohit/time-series-new")
@mock.patch("jovian.utils.commit.api.get_current_user", return_value={'username': 'rohit'})
@mock.patch("jovian.utils.commit.api.get_gist", side_effect=mock_get_gist)
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={"write": True})
def test_parse_project_from_rcfile(mock_get_gist_access, mock_get_gist, mock_get_current_user, mock_get_notebook_slug):
    with fake_creds():
        assert _parse_project(project=None, filename="file.ipynb", new_project=False) == ('demo-notebook', None)


@mock.patch("jovian.utils.commit.api.upload_file")
def test_attach_file(mock_upload_file):
    with temp_directory():
        os.system('touch tempfile.txt')

        _attach_file('tempfile.txt', 'fake_gist_slug', version=2)
        mock_upload_file.assert_called_with('fake_gist_slug', ('tempfile.txt', ANY), ANY, 2, False)


def test_attach_file_raises_error(capsys):
    with temp_directory():
        _attach_file('tempfile.txt', 'fake_gist_slug', version=2)

        expected_result = "[jovian] Error: [Errno 2] No such file or directory: 'tempfile.txt' (tempfile.txt)"
        captured = capsys.readouterr()
        assert captured.err.strip() == expected_result


@mock.patch("jovian.utils.commit._attach_file")
@pytest.mark.parametrize(
    "attach_files_kwargs, extra_config, mock_calls",
    [
        (
            {"paths": []},
            {},
            []
        ),
        (
            {"paths": ['tempdir']},
            {},
            [
                call('tempdir/file.txt', 'fake_gist_slug', 2, False),
                call('tempdir/subdir/file1.txt', 'fake_gist_slug', 2, False)
            ]
        ),
        (
            {"paths": "tempdir"},
            {},
            [
                call('tempdir/file.txt', 'fake_gist_slug', 2, False),
                call('tempdir/subdir/file1.txt', 'fake_gist_slug', 2, False)
            ]
        ),
        (
            {"paths": ['tempdir/file.txt', 'tempdir/subdir', 'tempdir/doesnotexist.txt']},
            {},
            [
                call('tempdir/file.txt', 'fake_gist_slug', 2, False),
                call('tempdir/subdir/file1.txt', 'fake_gist_slug', 2, False)
            ]
        ),
        (
            {"paths": []},
            {
                "DEFAULT_CONFIG": {
                    "UPLOAD_WORKING_DIRECTORY": True
                }
            },
            [
                call('notebook.ipynb', 'fake_gist_slug', 2, False),
                call('valid/file.txt', 'fake_gist_slug', 2, False),
                call('valid/file.ipynb', 'fake_gist_slug', 2, False),
                call('valid/file.tsv', 'fake_gist_slug', 2, False),
                call('valid/file.yaml', 'fake_gist_slug', 2, False),
                call('valid/file.yml', 'fake_gist_slug', 2, False),
                call('valid/file.py', 'fake_gist_slug', 2, False),
                call('valid/file.csv', 'fake_gist_slug', 2, False),
                call('tempdir/file.txt', 'fake_gist_slug', 2, False),
                call('tempdir/subdir/file1.txt', 'fake_gist_slug', 2, False)
            ]
        ),
        (
            {"paths": [], "output": True},
            {},
            []
        ),
        (
            {"paths": [], "output": True},
            {
                "DEFAULT_CONFIG": {
                    "UPLOAD_WORKING_DIRECTORY": True
                }
            },
            []
        ),
        (
            {"paths": [], "exclude_files": "notebook.ipynb"},
            {
                "DEFAULT_CONFIG": {
                    "UPLOAD_WORKING_DIRECTORY": True
                }
            },
            [
                call('valid/file.txt', 'fake_gist_slug', 2, False),
                call('valid/file.ipynb', 'fake_gist_slug', 2, False),
                call('valid/file.tsv', 'fake_gist_slug', 2, False),
                call('valid/file.yaml', 'fake_gist_slug', 2, False),
                call('valid/file.yml', 'fake_gist_slug', 2, False),
                call('valid/file.py', 'fake_gist_slug', 2, False),
                call('valid/file.csv', 'fake_gist_slug', 2, False),
                call('tempdir/file.txt', 'fake_gist_slug', 2, False),
                call('tempdir/subdir/file1.txt', 'fake_gist_slug', 2, False)
            ]
        ),
        (
            {
                "paths": [],
                "exclude_files": ["notebook.ipynb", "valid/file.txt", "tempdir/file.txt", "nonexistentfile.txt"]
            },
            {
                "DEFAULT_CONFIG": {
                    "UPLOAD_WORKING_DIRECTORY": True
                }
            },
            [
                call('valid/file.ipynb', 'fake_gist_slug', 2, False),
                call('valid/file.tsv', 'fake_gist_slug', 2, False),
                call('valid/file.yaml', 'fake_gist_slug', 2, False),
                call('valid/file.yml', 'fake_gist_slug', 2, False),
                call('valid/file.py', 'fake_gist_slug', 2, False),
                call('valid/file.csv', 'fake_gist_slug', 2, False),
                call('tempdir/subdir/file1.txt', 'fake_gist_slug', 2, False)
            ]
        ),
    ]
)
def test_attach_files(mock_attach_file, attach_files_kwargs, extra_config, mock_calls, capsys):
    with fake_creds(extra=extra_config):

        os.makedirs('tempdir/subdir')
        os.system('touch tempdir/file.txt && touch tempdir/subdir/file1.txt')

        # current notebook
        os.system('touch notebook.ipynb')

        # valid files
        os.mkdir('valid')
        valid_files = ["file.txt", "file.py", "file.csv", "file.yaml", "file.yml", "file.ipynb", "file.tsv"]
        for file in valid_files:
            os.system("touch valid/{}".format(file))

        # invalid files
        os.mkdir('invalid')
        invalid_files = ["file.file", "no_extension", "file.pyc"]
        for file in invalid_files:
            os.system("touch invalid/{}".format(file))

        _attach_files(gist_slug='fake_gist_slug', version=2, **attach_files_kwargs)

        mock_attach_file.assert_has_calls(mock_calls, any_order=True)


@mock.patch("jovian.utils.commit.upload_conda_env")
def test_capture_environment(mock_upload_conda_env):
    with fake_creds():
        _capture_environment('conda', 'fake_gist_slug', 2)

        mock_upload_conda_env.assert_called_with('fake_gist_slug', 2)


@pytest.mark.parametrize(
    "environment, env_config, mock_upload",
    [
        ("auto", "conda", "jovian.utils.commit.upload_conda_env"),
        ("auto", "pip", "jovian.utils.commit.upload_pip_env"),
    ]
)
def test_capture_environment_from_config(environment, env_config, mock_upload):
    with fake_creds(extra={"DEFAULT_CONFIG": {"environment": env_config}}), mock.patch(mock_upload) as mock_upload:
        _capture_environment(environment, 'fake_gist_slug', 2)
        mock_upload.assert_called_with('fake_gist_slug', 2)


@mock.patch("jovian.utils.commit.upload_pip_env")
@mock.patch("jovian.utils.commit.upload_conda_env")
def test_capture_environment_from_config_none(mock_upload_conda_env, mock_upload_pip_env):
    with fake_creds(extra={"DEFAULT_CONFIG": {"environment": None}}):
        _capture_environment("auto", "fake_gist_slug", 2)

        mock_upload_conda_env.assert_not_called()
        mock_upload_pip_env.assert_not_called()


@mock.patch("jovian.utils.commit.upload_pip_env")
@mock.patch("jovian.utils.commit.upload_conda_env")
def test_capture_environment_conda_error_and_pip_exception(mock_upload_conda_env, mock_upload_pip_env, capsys):

    def conda_error_raiser(*args, **kwargs):
        raise CondaError('fake conda error')

    def pip_exception_raiser(*args, **kwargs):
        raise Exception('fake pip error')

    mock_upload_conda_env.side_effect = conda_error_raiser
    mock_upload_pip_env.side_effect = pip_exception_raiser

    _capture_environment('auto', 'fake_gist_slug', 2)

    mock_upload_conda_env.assert_called_with('fake_gist_slug', 2)
    mock_upload_pip_env.assert_called_with('fake_gist_slug', 2)

    expected_result = dedent("""
            [jovian] Error: fake conda error
            [jovian] Error: fake pip error
            """).strip()
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result


@mock.patch("jovian.utils.commit.log_git")
def test_perform_git_commit(mock_log_git, capsys):
    with mock_git_repo():
        os.system("echo \"hello world\" >> file.txt")

        _perform_git_commit(filename='file.txt', git_commit=True, git_message='added file.txt')

        # Assert that commit took place
        assert os.popen('git show -s --format=%s HEAD').read().strip() == 'added file.txt'

        # Assert that it was logged
        expected_result = "[jovian] Git repository identified. Performing git commit..."
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result

        mock_log_git.assert_called_with(
            {
                'repository': 'https://github.com/JovianML/mock_repo',
                'commit': ANY,
                'filename': 'file.txt',
                'path': '.',
                'branch': 'master'
            },
            verbose=False
        )


@mock.patch("jovian.utils.commit.api.post_records")
def test_attach_records(mock_api_post_records, capsys):
    with fake_records():
        _attach_records('fake_gist_slug', 2)

        mock_api_post_records.assert_called_with(
            'fake_gist_slug',
            ['fake_slug_metrics_1', 'fake_slug_metrics_2', 'fake_slug_hyperparams_1', 'fake_slug_hyperparams_2'],
            2
        )

        expected_result = "[jovian] Attaching records (metrics, hyperparameters, dataset etc.)"
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


def test_list_ipynb_files(tmpdir, capsys):
    folder1 = tmpdir.mkdir("sub")
    folder2 = tmpdir.mkdir("sub2")
    file1 = folder1.join("test1.ipynb").ensure(file=True)
    file2 = folder1.join("test2.ipynb").ensure(file=True)
    file3 = folder1.join("test3.py").ensure(file=True)

    assert len(tmpdir.listdir()) == 2
    assert len(_list_ipynb_files(str(file1))) == 1
    assert len(_list_ipynb_files(str(file3))) == 0
    assert len(_list_ipynb_files(str(folder1))) == 2
    assert len(_list_ipynb_files(str(folder2))) == 0


@pytest.mark.parametrize(
    "ipynb_files, confirm, expected_files", [
        ([], True, []),
        ([], False, []),
        (["test1.ipynb"], True, ["test1.ipynb"]),
        (["test1.ipynb"], False, []),
        (["test1.ipynb", "test2.ipynb"], True, ["test1.ipynb", "test2.ipynb"]),
        (["test1.ipynb", "test2.ipynb"], False, []),
        (["test{}.ipynb".format(i) for i in range(0, 20)], True, ["test{}.ipynb".format(i) for i in range(0, 20)]),
        (["test{}.ipynb".format(i) for i in range(0, 20)], False, []),
        (["test{}.ipynb".format(i) for i in range(0, 50)], True, []),
        (["test{}.ipynb".format(i) for i in range(0, 50)], False, [])
    ]
)
@mock.patch("time.sleep")
@mock.patch("jovian.utils.commit.commit")
def test_commit_path(mock_commit, mock_sleep, ipynb_files, confirm, expected_files):
    with mock.patch("jovian.utils.commit._list_ipynb_files", return_value=ipynb_files) as mock_func:
        with mock.patch("click.confirm", return_value=confirm) as mock_confirm:
            commit_path(path="notebook", environment=None, is_cli=True)
            mock_commit.assert_has_calls([call(filename=f, environment=None, is_cli=True) for f in expected_files])


@pytest.mark.parametrize(
    "commit_kwargs, expected_result",
    [({"secret": True},
      """[jovian] Error: "secret" is deprecated. Use "privacy" instead (allowed options: "public", "private", "secret", "auto")"""),
     ({"nb_filename": 'file'},
      """[jovian] Error: "nb_filename" is deprecated. Use "filename" instead"""),
     ({"env_type": "conda"},
      """[jovian] Error: "env_type" is deprecated. Use "environment" instead"""),
     ({"capture_env": False},
      """[jovian] Error: "catpure_env" is deprecated. Use "environment=None" instead"""),
     ({"notebook_id": "fake_notebook_id"},
      """[jovian] Error: "notebook_id" is deprecated. Use "project" instead."""),
     ({"create_new": True},
      """[jovian] Error: "create_new" is deprecated. Use "new_project" instead."""),
     ({"artifacts": ['file1', 'file2']},
      """[jovian] Error: "artifacts" is deprecated. Use "outputs" instead"""), ])
@mock.patch("jovian.utils.commit.in_notebook", return_value=False)
@mock.patch("jovian.utils.commit.in_script", return_value=False)
def test_commit_deprecated_args(mock_in_script, mock_in_notebook, commit_kwargs, expected_result, capsys):

    commit(message="this is the first commit", **commit_kwargs)
    captured = capsys.readouterr()
    assert captured.err.strip() == \
        expected_result.strip() + """\n[jovian] Error: Failed to detect Jupyter notebook or Python script. Skipping.."""


@mock.patch("jovian.utils.commit.save_notebook", return_value=None)
@mock.patch("jovian.utils.commit._parse_filename", return_value=None)
@mock.patch("jovian.utils.commit.in_notebook", return_value=True)
@mock.patch("jovian.utils.commit.in_script", return_value=False)
def test_commit_in_notebook_filename_none(
        mock_in_script, mock_in_notebook, mock_parse_filename, mock_save_notebook, capsys):

    commit('initial commit')
    expected_result_out = dedent("""
    [jovian] Attempting to save notebook..""")
    expected_result_err = dedent("""
        [jovian] Error: Failed to detect notebook filename. Please provide the correct notebook filename as the "filename" argument to "jovian.commit".""")
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result_out.strip()
    assert captured.err.strip() == expected_result_err.strip()


@mock.patch("jovian.utils.commit.os.path.exists", return_value=False)
@mock.patch("jovian.utils.commit._parse_filename", return_value='file')
@mock.patch("jovian.utils.commit.in_notebook", return_value=False)
@mock.patch("jovian.utils.commit.in_script", return_value=True)
def test_commit_file_does_not_exist(
        mock_in_script, mock_in_notebook, mock_parse_filename, mock_os_path_exists, capsys):

    commit('initial commit')

    expected_result = """[jovian] Error: The detected/provided file "file" does not exist. Please provide the correct notebook filename as the "filename" argument to "jovian.commit"."""
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result.strip()


def mock_create_gist_simple(*args, **kwargs):
    data = {
        "slug": "fake_gist_slug",
        "title": "demo-notebook",
        "owner": {
                "avatar": "https://api-staging.jovian.ai/api/user/rohit/avatar",
                "id": 47,
                "name": "Rohit Sanjay",
                "username": "rohit"
        },
        "version": 2
    }
    return data


def patch_all(f):
    @mock.patch("jovian.utils.commit._attach_records")
    @mock.patch("jovian.utils.commit._perform_git_commit")
    @mock.patch("jovian.utils.commit._attach_files")
    @mock.patch("jovian.utils.commit._capture_environment")
    @mock.patch("jovian.utils.commit.set_notebook_slug")
    @mock.patch("jovian.utils.commit.read_webapp_url", return_value='https://staging.jovian.ml/')
    @mock.patch("jovian.utils.commit.api.create_gist_simple", side_effect=mock_create_gist_simple)
    @mock.patch("jovian.utils.commit._parse_project", return_value=('fake_project_title', 'fake_project_id'))
    @mock.patch("jovian.utils.commit.os.path.exists", return_value=True)
    @mock.patch("jovian.utils.commit._parse_filename", return_value='file')
    @mock.patch("jovian.utils.commit.in_notebook", return_value=False)
    @mock.patch("jovian.utils.commit.in_script", return_value=True)
    @functools.wraps(f)
    def functor(*args, **kwargs):
        return f(*args, **kwargs)
    return functor


@patch_all
def test_commit(mock_in_script,
                mock_in_notebook,
                mock_parse_filename,
                mock_os_path_exists,
                mock_parse_project,
                mock_create_gist_simple,
                mock_read_webapp_url,
                mock_set_notebook_slug,
                mock_capture_environment,
                mock_attach_files,
                mock_perform_git_commit,
                mock_attach_records,
                capsys):

    returned_value = commit('initial commit', files=['file1', 'file2', 'file3'], privacy='secret',
                            environment='conda', outputs=['model.h5', 'gen.csv'])

    mock_create_gist_simple.assert_called_with(
        'file', 'fake_project_id', 'secret', 'fake_project_title', 'initial commit')

    mock_set_notebook_slug.assert_called_with('file', 'fake_gist_slug')

    mock_capture_environment.assert_called_with('conda', 'fake_gist_slug', 2)

    _attach_files_calls = [call(['file1', 'file2', 'file3'], 'fake_gist_slug', 2, exclude_files='file'),
                           call(['model.h5', 'gen.csv'], 'fake_gist_slug', 2, output=True)]
    mock_attach_files.assert_has_calls(_attach_files_calls)

    mock_perform_git_commit.assert_called_with('file', False, 'initial commit')

    mock_attach_records.assert_called_with('fake_gist_slug', 2)

    expected_common_result = "[jovian] Committed successfully! https://staging.jovian.ml/rohit/demo-notebook"
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_common_result.strip()
    assert returned_value == "https://staging.jovian.ml/rohit/demo-notebook"
