import json
from time import sleep


from IPython import get_ipython
from jovian.utils.logger import log


def get_kaggle_notebook(project):
    """ Retreive all cells and writes it to a file called project-name.ipynb, then returns the filename"""

    jovian_temp = None
    get_ipython().run_cell_magic(
        'javascript',
        '',
        '''
        require(["base/js/namespace"],function(Jupyter) {
            const nb_cells = JSON.stringify(Jupyter.notebook.toJSON());
            Jupyter.notebook.kernel.execute('jovian_temp=r"""'+nb_cells+'"""');
        });
        ''')

    filename = '{}.ipynb'.format(project)
    sleep(2)

    if not jovian_temp:
        log("Failed to retrieve. Please report the issue.", error=True)
        return

    with open(filename, 'w') as f:
        f.write(jovian_temp)
    del jovian_temp

    return filename
