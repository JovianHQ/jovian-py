import os
import shutil
import pytest
import functools
from unittest import mock
from unittest.mock import ANY, call
from contextlib import contextmanager

from jovian.utils.commit import (_parse_filename, _parse_project, _attach_file,
                                 _attach_files, _capture_environment, _perform_git_commit, _attach_records, commit)
from jovian.tests.resources.shared import fake_creds, temp_directory, mock_git_repo, fake_records
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


@mock.patch("jovian.utils.commit.get_script_filename", return_value='fake-script.py')
@mock.patch("jovian.utils.commit.in_script", return_value=True)
def test_parse_filename_in_script(mock_in_script, mock_get_script_filename):
    assert _parse_filename(filename=None) == 'fake-script.py'

    assert _parse_filename('script.py') == 'script.py'

    assert _parse_filename('script.txt') == 'script.txt.py'


@mock.patch("jovian.utils.commit.in_script", return_value=False)
@mock.patch("jovian.utils.commit.get_notebook_name", return_value='fake-notebook.ipynb')
@mock.patch("jovian.utils.commit.in_notebook", return_value=True)
def test_parse_filename_in_notebook(mock_in_notebook, mock_get_script_name, mock_in_script):
    assert _parse_filename(filename=None) == 'fake-notebook.ipynb'

    assert _parse_filename('notebook.ipynb') == 'notebook.ipynb'

    assert _parse_filename('notebook.txt') == 'notebook.txt.ipynb'


@mock.patch("jovian.utils.commit.api.get_gist", side_effect=mock_get_gist)
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={'write': True})
@mock.patch("jovian.utils.commit._current_slug", "f67108fc906341d8b15209ce88ebc3d2")
def test_parse_project_in_memory(mock_current_slug, mock_get_gist_access):
    with fake_creds():
        assert _parse_project(
            project=None,
            filename='file.ipynb',
            new_project=False) == ('demo-notebook', 'f67108fc906341d8b15209ce88ebc3d2')


@mock.patch("jovian.utils.commit.api.get_gist", side_effect=mock_get_gist)
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={'write': True})
@mock.patch("jovian.utils.commit.get_notebook_slug", return_value="f67108fc906341d8b15209ce88ebc3d2")
def test_parse_project_from_jovianrc(mock_get_notebook_slug, mock_get_gist_access, mock_get_gist):
    with fake_creds():
        assert _parse_project(
            project=None,
            filename='file.ipynb',
            new_project=False) == ('demo-notebook', 'f67108fc906341d8b15209ce88ebc3d2')


def test_parse_project_none():
    with fake_creds():
        assert _parse_project(project=None, filename='file.ipynb', new_project=True) == (None, None)


@mock.patch("jovian.utils.commit.api.get_gist", side_effect=mock_get_gist)
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={'write': True})
@mock.patch("jovian.utils.commit.get_notebook_slug", return_value="f67108fc906341d8b15209ce88ebc3d2")
def test_parse_project_username_title(mock_get_notebook_slug, mock_get_gist_access, mock_get_gist):
    with fake_creds():
        assert _parse_project(
            project='rohit/time-series',
            filename='file.ipynb',
            new_project=True) == ('demo-notebook', 'f67108fc906341d8b15209ce88ebc3d2')


@mock.patch("jovian.utils.commit.api.get_gist", side_effect=mock_get_gist)
@mock.patch("jovian.utils.commit.api.get_current_user", return_value={'username': 'rohit'})
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={'write': True})
@mock.patch("jovian.utils.commit.get_notebook_slug", return_value="f67108fc906341d8b15209ce88ebc3d2")
def test_parse_project_only_title(mock_get_notebook_slug, mock_get_gist_access, mock_get_current_user, mock_get_gist):
    with fake_creds():
        assert _parse_project(
            project='time-series',
            filename='file.ipynb',
            new_project=True) == ('demo-notebook', 'f67108fc906341d8b15209ce88ebc3d2')


@mock.patch("jovian.utils.commit.api.get_gist", return_value=None)
@mock.patch("jovian.utils.commit.api.get_current_user", return_value={'username': 'rohit'})
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={'write': True})
@mock.patch("jovian.utils.commit.get_notebook_slug", return_value="f67108fc906341d8b15209ce88ebc3d2")
def test_parse_project_only_title_no_metadata(
        mock_get_notebook_slug, mock_get_gist_access, mock_get_current_user, mock_get_gist):
    with fake_creds():
        assert _parse_project(
            project='time-series',
            filename='file.ipynb',
            new_project=True) == ('time-series', None)


@mock.patch("jovian.utils.commit.api.get_gist", side_effect=mock_get_gist)
@mock.patch("jovian.utils.commit.api.get_current_user", return_value={'username': 'rohit'})
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={'write': False})
@mock.patch("jovian.utils.commit.get_notebook_slug", return_value="f67108fc906341d8b15209ce88ebc3d2")
def test_parse_project_only_title_no_metadata_no_commit_permission(
        mock_get_notebook_slug, mock_get_gist_access, mock_get_current_user, mock_get_gist):
    with fake_creds():
        assert _parse_project(
            project='time-series',
            filename='file.ipynb',
            new_project=True) == ('demo-notebook', None)


@mock.patch("jovian.utils.commit.api.get_gist", side_effect=mock_get_gist)
@mock.patch("jovian.utils.commit.api.get_gist_access", return_value={'write': True})
@mock.patch("jovian.utils.commit.get_notebook_slug", return_value="f67108fc906341d8b15209ce88ebc3d2")
def test_parse_project_project_id_none(mock_get_notebook_slug, mock_get_gist_access, mock_get_gist):
    with fake_creds():
        assert _parse_project(
            project='rohit/time-series-new',
            filename='file.ipynb',
            new_project=True) == ('demo-notebook', None)


@mock.patch("jovian.utils.commit.api.upload_file")
def test_attach_file(mock_upload_file):
    # setUp
    os.system('touch tempfile.txt')

    try:
        _attach_file('tempfile.txt', 'fake_gist_slug', version=2)
        mock_upload_file.assert_called_with('fake_gist_slug', ('tempfile.txt', ANY), ANY, 2, False)
    finally:
        # tearDown
        os.system('rm tempfile.txt')


def mock_upload_file(*args, **kwargs):
    raise Exception('fake error')


@mock.patch("jovian.utils.commit.api.upload_file", side_effect=mock_upload_file)
def test_attach_file_raises_error(mock_upload_file, capsys):

    _attach_file('tempfile.txt', 'fake_gist_slug', version=2)

    expected_result = "[jovian] Error: [Errno 2] No such file or directory: 'tempfile.txt' (tempfile.txt)"
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result


@mock.patch("jovian.utils.commit._attach_file")
@pytest.mark.parametrize(
    "files, mock_calls",
    [
        ([], []),
        (['tempdir'], [
            call('tempdir/file.txt', 'fake_gist_slug', 2, False),
            call('tempdir/tempdir1/file1.txt', 'fake_gist_slug', 2, False)
        ]),
        ('tempdir', [
            call('tempdir/file.txt', 'fake_gist_slug', 2, False),
            call('tempdir/tempdir1/file1.txt', 'fake_gist_slug', 2, False)
        ]),
        (['tempdir/file.txt', 'tempdir/tempdir1', 'tempdir/doesnotexist.txt'], [
            call('tempdir/file.txt', 'fake_gist_slug', 2, False),
            call('tempdir/tempdir1/file1.txt', 'fake_gist_slug', 2, False)
        ]),
    ]
)
def test_attach_files(mock_attach_file, files, mock_calls, capsys):
    with fake_creds(), temp_directory():
        # setUp
        os.mkdir('tempdir')
        os.mkdir('tempdir/tempdir1')
        os.system('touch tempdir/file.txt && touch tempdir/tempdir1/file1.txt')

        _attach_files(files, 'fake_gist_slug', 2)
        mock_attach_file.assert_has_calls(mock_calls)


@mock.patch("jovian.utils.commit.upload_conda_env")
def test_capture_environment(mock_upload_conda_env):
    _capture_environment('conda', 'fake_gist_slug', 2)
    mock_upload_conda_env.assert_called_with('fake_gist_slug', 2)


def conda_error_raiser(*args, **kwargs):
    raise CondaError('fake error')


@mock.patch("jovian.utils.commit.upload_pip_env")
@mock.patch("jovian.utils.commit.upload_conda_env", side_effect=conda_error_raiser)
def test_capture_environment_conda_error(mock_upload_conda_env, mock_upload_pip_env, capsys):
    _capture_environment('auto', 'fake_gist_slug', 2)
    mock_upload_conda_env.assert_called_with('fake_gist_slug', 2)
    mock_upload_pip_env.assert_called_with('fake_gist_slug', 2)

    expected_result = "[jovian] Error: fake error"
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result


def pip_exception_raiser(*args, **kwargs):
    raise Exception('fake exception')


@mock.patch("jovian.utils.commit.upload_pip_env", side_effect=pip_exception_raiser)
@mock.patch("jovian.utils.commit.upload_conda_env", side_effect=conda_error_raiser)
def test_capture_environment_conda_error_and_pip_exception(mock_upload_conda_env, mock_upload_pip_env, capsys):
    _capture_environment('auto', 'fake_gist_slug', 2)
    mock_upload_conda_env.assert_called_with('fake_gist_slug', 2)
    mock_upload_pip_env.assert_called_with('fake_gist_slug', 2)

    expected_result = "[jovian] Error: fake error\n[jovian] Error: fake exception"
    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result


def mock_api_post_block(*args, **kwargs):
    data = {
        'count': 1,
        'tracking': {
            'createdAt': 1577270059593,
            'updatedAt': None, 'gistSlug': None,
            'trackingSlug': 'fake_slug_3',
            'gistVersion': None
        }
    }

    return data


@mock.patch("jovian.utils.records.api.post_block", side_effect=mock_api_post_block)
def test_perform_git_commit(mock_api_post_block, capsys):
    with mock_git_repo():
        os.system("echo \"hello world\" >> file.txt")
        _perform_git_commit(filename='file.txt', git_commit=True, git_message='added file.txt')

        assert os.popen('git show -s --format=%s HEAD').read().strip() == 'added file.txt'

        expected_result = "[jovian] Git repository identified. Performing git commit..."
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.commit.api.post_records")
def test_attach_records(mock_api_post_records, capsys):
    with fake_records():
        _attach_records('fake_gist_slug', 2)

        mock_api_post_records.assert_called_with(
            'fake_gist_slug',
            ['fake_slug_metrics_1', 'fake_slug_metrics_2', 'fake_slug_hyperparams_1', 'fake_slug_hyperparams_2'],
            2)

        expected_result = "[jovian] Attaching records (metrics, hyperparameters, dataset etc.)"
        captured = capsys.readouterr()
        assert captured.out.strip() == expected_result


@mock.patch("jovian.utils.commit.in_notebook", return_value=False)
@mock.patch("jovian.utils.commit.in_script", return_value=False)
def test_commit_deprecated_args_unsupported_environment(mock_in_script, mock_in_notebook, capsys):

    commit(
        message="this is the first commit",
        secret=True,
        nb_filename='file',
        env_type="conda",
        capture_env=False,
        notebook_id='fake_notebook_id',
        create_new=True,
        artifacts=['file1', 'file2'])

    expected_result = """
[jovian] Error: "secret" is deprecated. Use "privacy" instead (allowed options: "public", "private", "secret", "auto")
[jovian] Error: "nb_filename" is deprecated. Use "filename" instead
[jovian] Error: "env_type" is deprecated. Use "environment" instead
[jovian] Error: "catpure_env" is deprecated. Use "environment=None" instead
[jovian] Error: "notebook_id" is deprecated. Use "project" instead.
[jovian] Error: "create_new" is deprecated. Use "new_project" instead.
[jovian] Error: "artifacts" is deprecated. Use "outputs" instead
[jovian] Error: Failed to detect Jupyter notebook or Python script. Skipping.."""

    captured = capsys.readouterr()
    assert captured.err.strip() == expected_result.strip()


@mock.patch("jovian.utils.commit.save_notebook", return_value=None)
@mock.patch("jovian.utils.commit._parse_filename", return_value=None)
@mock.patch("jovian.utils.commit.in_notebook", return_value=True)
@mock.patch("jovian.utils.commit.in_script", return_value=False)
def test_commit_in_notebook_filename_none(
        mock_in_script, mock_in_notebook, mock_parse_filename, mock_save_notebook, capsys):

    commit('initial commit')

    expected_result = """
[jovian] Attempting to save notebook..
[jovian] Failed to detect notebook filename. Please provide the correct notebook filename as the "filename" argument to "jovian.commit"."""
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()


@mock.patch("jovian.utils.commit.os.path.exists", return_value=False)
@mock.patch("jovian.utils.commit._parse_filename", return_value='file')
@mock.patch("jovian.utils.commit.in_notebook", return_value=False)
@mock.patch("jovian.utils.commit.in_script", return_value=True)
def test_commit_file_does_not_exist(
        mock_in_script, mock_in_notebook, mock_parse_filename, mock_os_path_exists, capsys):

    commit('initial commit')

    expected_result = """[jovian] The detected/provided file "file" does not exist. Please provide the correct notebook filename as the "filename" argument to "jovian.commit"."""
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()


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

    commit('initial commit', files=['file1', 'file2', 'file3'], privacy='secret',
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

    expected_result = "[jovian] Committed successfully! https://staging.jovian.ml/rohit/demo-notebook"
    captured = capsys.readouterr()
    assert captured.out.strip() == expected_result.strip()
