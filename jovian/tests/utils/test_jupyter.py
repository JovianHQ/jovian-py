from unittest import TestCase, mock
from jovian.utils.jupyter import has_ipynb_shell, in_notebook, get_notebook_server_path


class MockResponse:
    def __init__(self, json_data, status_code, text=""):
        self.json_data = json_data
        self.status_code = status_code
        self.text = text

    def json(self):
        return self.json_data


def mock_requests_get(url, *args, **kwargs):
    if url == 'http://localhost:8888/api/sessions?token=70d4914ffeb1a2cd0d0943a4255568b3a3dd053e9c28516d':
        data = [
            {'name': '', 'notebook': {'name': '', 'path': 'Untitled.ipynb'},
             'path': 'Untitled.ipynb', 'id': '02c8f6cd-6476-4661-8cdf-21d4b275328e',
             'kernel':
             {'connections': 1, 'name': 'python3', 'execution_state': 'idle',
              'id': '3df6eb89-39d3-4636-a831-b2b9db28eb4e', 'last_activity': '2020-01-23T19:08:12.933167Z'},
             'type': 'notebook'}]
        text = '[{"name": "", "notebook": {"name": "", "path": "Untitled.ipynb"}, "path": "Untitled.ipynb", "id": "02c8f6cd-6476-4661-8cdf-21d4b275328e", "kernel": {"connections": 1, "name": "python3", "execution_state": "idle", "id": "3df6eb89-39d3-4636-a831-b2b9db28eb4e", "last_activity": "2020-01-23T19:08:12.933167Z"}, "type": "notebook"}]'
        return MockResponse(data, 200, )


@mock.patch("IPython.get_ipython")
def test_has_ipynb_shell_true(mock_get_ipython):
    mock_get_ipython().__class__.__name__ = 'ZMQInteractiveShell'
    assert has_ipynb_shell() == True


@mock.patch("IPython.get_ipython")
def test_has_ipynb_shell_terminal(mock_get_ipython):
    mock_get_ipython().__class__.__name__ = 'TerminalInteractiveShell'
    assert has_ipynb_shell() == False


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
