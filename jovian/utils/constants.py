# URLs for public versions of Jovian
DEFAULT_WEBAPP_URL = "https://jovian.ml/"
DEFAULT_API_URL = "https://api.jovian.ai/"

RC_FILENAME = ".jovianrc"
FILENAME_MSG = 'Failed to detect notebook filename. Please provide the notebook filename ' + \
    '(including .ipynb extension) as the "nb_filename" argument to "jovian.commit".'
ISSUES_MSG = """NOTE: Jovian is currently in beta, so if you face any issues, 
      please report them here: https://github.com/JovianML/jovian-py/issues"""

LINUX = 'linux'
WINDOWS = 'windows'
MACOS = 'macos'
PLATFORMS = [LINUX, WINDOWS, MACOS]

STORAGE_ALLOWED_EXTENSIONS = tuple('ipynb yml yaml py txt csv'.split())

DEFAULT_ORG_ID = "public"
