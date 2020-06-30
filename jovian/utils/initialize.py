from jovian.utils.colab import in_colab
from jovian.utils.jupyter import set_notebook_name
from jovian.utils.latest import check_update


def _initialize_jovian():
    """Initialize by setting the notebook name and checking for updates"""
    set_notebook_name()
    check_update()
    if in_colab():
        print(globals())
        print("in colab")
        global id
        print(id)
