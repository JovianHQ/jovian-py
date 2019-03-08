"""Jupyter related utilities"""
from requests.compat import urljoin
import json
import os.path
import re
import requests
import time
from io import StringIO
import sys


def has_ipynb_shell():
    """Check if IPython shell is available"""
    try:
        from IPython import get_ipython
        cls = get_ipython().__class__.__name__
        return cls == 'ZMQInteractiveShell'
    except:
        return False


def in_notebook():
    """Check if this code is being executed in a notebook"""
    if not has_ipynb_shell():
        return False
    from ipykernel.kernelapp import IPKernelApp
    return IPKernelApp.initialized()


def get_notebook_server_path():
    try:  # Python 3
        from notebook.notebookapp import list_running_servers
    except ImportError:  # Python 2
        import warnings
        from IPython.utils.shimmodule import ShimWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ShimWarning)
            from IPython.html.notebookapp import list_running_servers

    """Get the path of the notebook relative to the Jupyter server"""
    import ipykernel
    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        for nn in json.loads(response.text):
            if nn['kernel']['id'] == kernel_id:
                relative_path = nn['notebook']['path']
                return relative_path


def get_notebook_path_py():
    try:  # Python 3
        from notebook.notebookapp import list_running_servers
    except ImportError:  # Python 2
        import warnings
        from IPython.utils.shimmodule import ShimWarning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ShimWarning)
            from IPython.html.notebookapp import list_running_servers

    import ipykernel
    """Get the full path of the jupyter notebook."""
    kernel_id = re.search('kernel-(.*).json',
                          ipykernel.connect.get_connection_file()).group(1)
    servers = list_running_servers()
    for ss in servers:
        response = requests.get(urljoin(ss['url'], 'api/sessions'),
                                params={'token': ss.get('token', '')})
        if response.status_code == 200:
            for nn in json.loads(response.text):
                if nn["kernel"] and nn['kernel']['id'] == kernel_id:
                    relative_path = nn['notebook']['path']
                    return os.path.join(ss['notebook_dir'], relative_path)


def get_notebook_path():
    nb_name = None
    # Try getting the notebook name using IPython API
    try:
        nb_name = get_notebook_path_py()
    except:
        pass

    # Try using Javascript instead
    if nb_name is None:
        saved_name = get_notebook_name_saved()
        if saved_name:
            nb_name = os.path.join(os.getcwd(), saved_name)

    return nb_name


def set_notebook_name():
    if in_notebook():
        from IPython import get_ipython
        get_ipython().run_cell_magic('javascript',
                                     '', "if (window.IPython && IPython.notebook.kernel) IPython.notebook.kernel.execute('jovian.utils.jupyter.get_notebook_name_saved = lambda: \"' + IPython.notebook.notebook_name + '\"')")


def get_notebook_name_saved():
    return None


def get_notebook_name():
    """Return the name of the notebook"""
    nb_path = get_notebook_path()
    if nb_path:
        return os.path.basename(nb_path)
    return None


def get_notebook_history():
    from IPython import get_ipython
    """Return full code history of notebook"""
    return get_ipython().magic('%history')


def save_notebook():
    from IPython import get_ipython
    """Save the current Jupyter notebook"""
    return get_ipython().run_cell_magic('javascript', '', 'window.require && require(["base/js/namespace"],function(Jupyter){Jupyter.notebook.save_checkpoint()})')
