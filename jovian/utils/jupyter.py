from requests.compat import urljoin
"""Jupyter related utilities"""
import json
import os.path
import re
import requests
import time
# from IPython.display import Javascript as d_js
from io import StringIO
import sys
# from IPython.utils import io

notebookName = None
isNotebookNameSet = False


class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


def has_ipynb_shell():
    """Check if IPython shell is available"""
    from IPython import get_ipython
    try:
        cls = get_ipython().__class__.__name__
        return cls == 'ZMQInteractiveShell'
    except NameError:
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


def get_notebook_path():
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
        else:
            return os.path.join(os.getcwd(), get_notebook_name_saved())


def set_notebook_name():
    from IPython import get_ipython
    get_ipython().run_cell_magic('javascript',
                                 '', "IPython.notebook.kernel.execute('nb_name = \"' + IPython.notebook.notebook_name + '\"')")


def get_notebook_name_saved():
    from IPython import get_ipython
    with Capturing() as cap:
        list(get_ipython().run_code(
            'print(globals()["nb_name"]) if "nb_name" in globals().keys() else None'))
    if len(cap) > 0:
        return cap[0]
    else:
        return None


def get_notebook_name():
    """Return the name of the notebook"""
    return os.path.basename(get_notebook_path())


def get_notebook_history():
    from IPython import get_ipython
    """Return full code history of notebook"""
    return get_ipython().magic('%history')


def save_notebook():
    from IPython import get_ipython
    """Save the current Jupyter notebook"""
    return get_ipython().run_cell_magic('javascript', '', 'require(["base/js/namespace"],function(Jupyter){Jupyter.notebook.save_checkpoint()})')
