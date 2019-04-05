WEBAPP_URL = "https://jvn.io"
API_URL = "https://api.jovian.ai"
RC_FILENAME = ".jovianrc"
FILENAME_MSG = 'Failed to detect notebook filename. Please provide the notebook filename (including .ipynb extension) as the "nb_filename" argument to "jovian.commit".'
ISSUES_MSG = """NOTE: Jovian is current in beta, so if you face any issues, 
      please report them here: https://github.com/swiftace-ai/jovian-py/issues"""

LINUX = 'linux'
WINDOWS = 'windows'
MACOS = 'macos'

PLATFORMS = [LINUX, WINDOWS, MACOS]

API_KEY = "API_KEY"
GUEST_KEY = "GUEST_KEY"
STORAGE_ALLOWED_EXTENSIONS = tuple('ipynb yml yaml py txt csv'.split())
