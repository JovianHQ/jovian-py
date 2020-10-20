# URLs for public versions of Jovian
DEFAULT_WEBAPP_URL = "https://jovian.ai/"
DEFAULT_API_URL = "https://api.jovian.ai/"

RC_FILENAME = ".jovianrc"
FILENAME_MSG = 'Failed to detect notebook filename. Please provide the correct notebook filename ' + \
    'as the "filename" argument to "jovian.commit".'
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
