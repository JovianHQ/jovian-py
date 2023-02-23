# URLs for public versions of Jovian
DEFAULT_WEBAPP_URL = "https://jovian.com/"
DEFAULT_API_URL = "https://api.jovian.com/"

RC_FILENAME = ".jovianrc"
FILENAME_MSG = 'Failed to read the Jupyter notebook. Please re-run this cell to try again. If the issue persists, provide ' + \
    'the "filename" argument to "jovian.commit" e.g. "jovian.commit(filename=\'my-notebook.ipynb\')"'
ISSUES_MSG = """NOTE: Jovian is currently in beta, so if you face any issues, 
               please report them here: https://github.com/JovianML/jovian-py/issues"""

LINUX = 'linux'
WINDOWS = 'windows'
MACOS = 'macos'
PLATFORMS = [LINUX, WINDOWS, MACOS]

STORAGE_ALLOWED_EXTENSIONS = tuple('ipynb yml yaml py txt csv'.split())

DEFAULT_ORG_ID = "public"

CONDA_NOT_FOUND = 'Anaconda binary not found. Please make sure the "conda" command is in your ' \
                  'system PATH or the environment variable $CONDA_EXE points to the anaconda binary'

DEFAULT_EXTENSION_WHITELIST = [".ipynb", ".yml", ".yaml", ".py", ".txt", ".csv", ".tsv"]
