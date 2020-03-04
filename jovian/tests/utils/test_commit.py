import os
import shutil
import pytest
from unittest import mock
from unittest.mock import ANY, call
from contextlib import contextmanager

from jovian.utils.commit import (_parse_filename, _parse_project, _attach_file,
                                 _attach_files, _capture_environment, _perform_git_commit, _attach_records, commit)
from jovian.tests.resources import fake_creds
from jovian.utils.error import CondaError


@contextmanager
def mock_git_repo():
    os.mkdir('mock_git_repo')
    os.chdir('mock_git_repo')
    os.system("""git init
    mkdir -p ./nested/folder/deep && touch ./nested/folder/deep/sample.ipynb""")
    os.chdir('nested/folder/deep')
    os.system('git add . && git commit -m "initial commit"')
    try:
        yield
    finally:
        os.chdir('../../../../')
        shutil.rmtree('mock_git_repo')


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
def test_attach_files(mock_attach_file, capsys):
    # setUp
    os.mkdir('tempdir')
    os.mkdir('tempdir/tempdir1')
    os.system('touch tempdir/file.txt && touch tempdir/tempdir1/file1.txt')

    try:
        _attach_files([], 'fake_gist_slug', 2)
        captured = capsys.readouterr()
        assert captured.out.strip() == ''

        _attach_files(['tempdir'], 'fake_gist_slug', 2)
        calls = [
            call('tempdir/file.txt', 'fake_gist_slug', 2, False),
            call('tempdir/tempdir1/file1.txt', 'fake_gist_slug', 2, False)
        ]
        mock_attach_file.assert_has_calls(calls)

        _attach_files(['tempdir/file.txt', 'tempdir/tempdir1', 'tempdir/doesnotexist.txt'], 'fake_gist_slug', 2)
        calls = [
            call('tempdir/file.txt', 'fake_gist_slug', 2, False),
            call('tempdir/tempdir1/file1.txt', 'fake_gist_slug', 2, False)
        ]
        mock_attach_file.assert_has_calls(calls)

        _attach_files('tempdir', 'fake_gist_slug', 2)
        calls = [
            call('tempdir/file.txt', 'fake_gist_slug', 2, False),
            call('tempdir/tempdir1/file1.txt', 'fake_gist_slug', 2, False)
        ]
        mock_attach_file.assert_has_calls(calls)

    finally:
        # tearDown
        shutil.rmtree('tempdir')


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


@contextmanager
def fake_records():
    import jovian.utils.records
    _d = jovian.utils.records._data_blocks
    jovian.utils.records._data_blocks = [('fake_slug_metrics_1', 'metrics', {}),
                                         ('fake_slug_metrics_2', 'metrics', {}),
                                         ('fake_slug_hyperparams_1', 'hyperparams', {}),
                                         ('fake_slug_hyperparams_2', 'hyperparams', {})]

    try:
        yield
    finally:
        jovian.utils.records._data_blocks = _d


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
