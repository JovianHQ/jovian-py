import os
import click
from requests import get

from jovian._version import __version__
from jovian.utils.constants import ISSUES_MSG

from jovian.utils.credentials import get_guest_key, read_api_key_opt, read_api_url, read_org_id
from jovian.utils.logger import log
from jovian.utils.rcfile import get_rcdata, rcfile_exists, set_notebook_slug
from jovian.utils.request import pretty
from jovian.utils.misc import urljoin


def _u(path):
    """Make a URL from the path"""
    return urljoin(read_api_url(), path)


def _h(fresh):
    """Create a header to provide library metadata"""
    api_key, _ = read_api_key_opt()

    headers = {"x-jovian-source": "library",
               "x-jovian-library-version": __version__,
               "x-jovian-command": "clone" if fresh else "pull",
               "x-jovian-guest": get_guest_key(),
               "x-jovian-org": read_org_id()}

    if api_key is not None:
        headers["Authorization"] = "Bearer " + api_key

    return headers


def _v(version):
    """Create version query parameter string"""
    if version is not None:
        return "?gist_version=" + str(version)
    return ""


def get_gist(slug, version, fresh):
    """Download a gist"""
    if '/' in slug:
        parts = slug.split('/')
        username, title = parts[0], parts[1]
        url = _u('user/' + username + '/gist/' + title + _v(version))
    else:
        url = _u('gist/' + slug + _v(version))
    res = get(url, headers=_h(fresh))
    if res.status_code == 200:
        return res.json()['data']
    raise Exception('Failed to retrieve Gist: ' + pretty(res))


def post_clone_msg(title):

    log("Cloned successfully to '{}'".format(title), color='green')
    log(click.style('\nNext steps:', fg='yellow', underline=True) +
        click.style("""
  $ cd {}                     
  $ jovian install            
  $ conda activate <env_name> 
  $ jupyter notebook
""".format(title), bold=True), pre=False)

    log("""
Replace <env_name> with the name of your environment (without the '<' & '>')
Jovian uses Anaconda ( https://conda.io/ ) under the hood,
so please make sure you have it installed and added to path.
* If you face issues with `jovian install`, try `conda env update`.
* If you face issues with `conda activate`, try `source activate <env_name>`
  or `activate <env_name>` to activate the virtual environment.
""", pre=False)


def clone(slug, version=None, fresh=True, include_outputs=True):
    """Download the files for a gist"""
    # Print issues link
    log(ISSUES_MSG)

    # Download gist metadata
    ver_str = '(version ' + version + ')' if version else ''
    log('Fetching ' + slug + " " + ver_str + "..")
    gist = get_gist(slug, version, fresh)
    title = gist['title']

    # If fresh clone, create directory
    if fresh:
        if os.path.exists(title):
            i = 1
            while os.path.exists(title + '-' + str(i)):
                i += 1
            title = title + '-' + str(i)
        if not os.path.exists(title):
            os.makedirs(title)
        os.chdir(title)

    # Download the files
    log('Downloading files..')
    for f in gist['files']:
        if not f['artifact'] or include_outputs:
            with open(f['filename'], 'wb') as fp:
                fp.write(get(f['rawUrl']).content)

        # Create .jovianrc for a fresh clone
        if fresh and f['filename'].endswith('.ipynb'):
            set_notebook_slug(f['filename'], slug)

    # Print success message and instructions
    if fresh:
        post_clone_msg(title)
    else:
        log('Files dowloaded successfully in current directory')


RCFILE_NOTFOUND = "Could not detect '.jovianrc' file. Make sure you are running 'jovian pull' inside a directory cloned with 'jovian clone'."


def pull(slug=None, version=None):
    """Get the latest files associated with the current gist"""
    # If a slug is provided, just use that
    if slug:
        clone(slug, version, fresh=False)
        return

    # Check if .jovianrc exists
    if not rcfile_exists():
        log(RCFILE_NOTFOUND, error=True)
        return

    # Get list of notebooks
    nbs = get_rcdata()['notebooks']
    for fname in nbs:
        # Get the latest files for each notebook
        clone(nbs[fname]['slug'], version, fresh=False)
