import json
from time import sleep


from IPython import get_ipython
from jovian.utils.logger import log


def get_kaggle_notebook(project):
    """ Retreive all cells and writes it to a file called project-name.ipynb, then returns the filename"""

    get_ipython().run_cell_magic(
        'javascript',
        '',
        '''
        require(["base/js/namespace"],function(Jupyter) {
            const nb_cells = JSON.stringify(Jupyter.notebook.toJSON());
            const code = `
with open("kaggle-notebook.ipynb", 'w') as f:
    f.write(r"""${nb_cells}""")`;
            Jupyter.notebook.kernel.execute(code);});''')

    sleep(1)
    filename = '{}.ipynb'.format(project)

    return filename
