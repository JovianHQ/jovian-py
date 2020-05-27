import json
from unittest import TestCase, mock

import pytest

from jovian.tests.resources.shared import MockResponse
from jovian.utils.jupyter import (
    get_notebook_server_path, has_ipynb_shell, in_notebook, get_notebook_path_py, get_notebook_path, set_notebook_name,
    get_notebook_name_saved, get_notebook_name, get_notebook_history, save_notebook)


@pytest.mark.parametrize(
    "get_ipython, expected_result",
    [
        ('ZMQInteractiveShell', True),
        ('TerminalInteractiveShell', False)
    ]
)
@mock.patch("IPython.get_ipython")
def test_has_ipynb_shell(mock_get_ipython, get_ipython, expected_result):
    mock_get_ipython().__class__.__name__ = get_ipython
    assert has_ipynb_shell() == expected_result


@mock.patch('builtins.__import__', return_value=ImportError('fake import error'))
@mock.patch("IPython.get_ipython")
def test_has_ipynb_shell_except_return_false(mock_get_ipython, mock_import):
    assert has_ipynb_shell() == False


@mock.patch("ipykernel.kernelapp.IPKernelApp")
@mock.patch("IPython.get_ipython")
def test_in_notebook_false(mock_get_ipython, mock_IPKernelApp):
    mock_get_ipython().__class__.__name__ = 'ZMQInteractiveShell'
    mock_IPKernelApp.initialized.return_value = False
    assert in_notebook() == False

    mock_IPKernelApp.initialized.return_value = True
    assert in_notebook() == True


def mock_list_running_servers():
    return [{'base_url': '/', 'hostname': 'localhost', 'notebook_dir': '/Users/rohitsanjay', 'password': False, 'pid': 20604,
             'port': 8888, 'secure': False, 'token': '87b9edfc60e39cda411857a364d3948b999e9cbec22b4f58',
             'url': 'http://localhost:8888/'}]


def mock_request_get(*args, **kwargs):
    data = [
        {
            "id": "6492b857-8ea0-45af-a1ab-8769dd066235",
            "path": "Untitled.ipynb",
            "name": "",
            "type": "notebook",
            "kernel": {
                "id": "ee27a181-852b-4f21-a2c0-a34eacef769c",
                "name": "python3",
                "last_activity": "2020-03-02T08:00:15.767476Z",
                "execution_state": "idle",
                "connections": 1},
            "notebook": {
                "path": "Fake-Notebook.ipynb",
                "name": ""
            }
        }
    ]

    return MockResponse(data, 200, json.dumps(data))


def mock_re():
    ret1 = mock.Mock()
    ret1().group.return_value = "ee27a181-852b-4f21-a2c0-a34eacef769c"
    return ret1


@pytest.mark.parametrize(
    "func, expected_result",
    [
        (get_notebook_server_path, 'Fake-Notebook.ipynb'),
        (get_notebook_path_py, '/Users/rohitsanjay/Fake-Notebook.ipynb'),
        (get_notebook_path, '/Users/rohitsanjay/Fake-Notebook.ipynb'),
    ]
)
@mock.patch("ipykernel.connect.get_connection_file", return_value='')
@mock.patch("re.search", side_effect=mock_re())
@mock.patch("notebook.notebookapp.list_running_servers", return_value=mock_list_running_servers())
@mock.patch("requests.get", side_effect=mock_request_get)
def test_notebook_path_funs(mock_get, mock_servers, mock_re, mock_get_connection_file, func, expected_result):
    assert func() == expected_result


@mock.patch("jovian.utils.jupyter.get_notebook_name_saved", return_value="Fake-Notebook.ipynb")
@mock.patch("os.getcwd", return_value="/Users/rohitsanjay")
def test_get_notebook_path_javascript(mock_getcwd, mock_get_notebook_name_saved):
    assert get_notebook_path() == '/Users/rohitsanjay/Fake-Notebook.ipynb'


@mock.patch('IPython.get_ipython')
@mock.patch("jovian.utils.jupyter.in_notebook", return_value=True)
def test_set_notebook_name(mock_in_notebook, mock_get_ipython):
    set_notebook_name()

    mock_get_ipython().run_cell_magic.assert_called_with('javascript', '',
                                                         "if (window.IPython && IPython.notebook.kernel) IPython.notebook.kernel.execute('jovian.utils.jupyter.get_notebook_name_saved = lambda: \"' + IPython.notebook.notebook_name + '\"')")


def test_get_notebook_name_saved():
    assert get_notebook_name_saved() == None


@mock.patch("jovian.utils.jupyter.get_notebook_path", side_effect=['/Users/rohitsanjay/Fake-Notebook.ipynb', None])
def test_get_notebook(mock_get_notebook_path):
    assert get_notebook_name() == 'Fake-Notebook.ipynb'

    assert get_notebook_name() == None


@mock.patch('IPython.get_ipython')
def test_get_notebook_history(mock_get_ipython):
    get_notebook_history()

    mock_get_ipython().magic.assert_called_with('%history')


@mock.patch('IPython.get_ipython')
@mock.patch("jovian.utils.jupyter.in_notebook", return_value=True)
def test_save_notebook(mock_in_notebook, mock_get_ipython):
    save_notebook()

    mock_get_ipython().run_cell_magic.assert_called_with(
        'javascript',
        '',
        'window.require && require(["base/js/namespace"],function(Jupyter){Jupyter.notebook.save_checkpoint()})')
