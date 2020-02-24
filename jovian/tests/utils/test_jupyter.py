from unittest import TestCase, mock

from jovian.utils.jupyter import get_notebook_server_path, has_ipynb_shell, in_notebook


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
