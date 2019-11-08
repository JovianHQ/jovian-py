import os


def setup_extension(enable=True):
    if enable:
        os.system("jupyter nbextension enable jovian_nb_ext/main --sys-prefix")
    else:
        os.system("jupyter nbextension disable jovian_nb_ext/main --sys-prefix")
