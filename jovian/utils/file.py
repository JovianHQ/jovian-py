import os
from collections import OrderedDict

from jovian.utils.api import upload_file
from jovian.utils.logger import log


def expand_files_list(files_list, dedupe=True):
    """Enumerate list of files from list of user input file/folder list"""
    result = []
    for fname in files_list:
        if os.path.exists(fname) and not os.path.isdir(fname):
            result.append(fname)
        elif os.path.isdir(fname):
            for folder, _, flist in os.walk(fname):
                for file in flist:
                    result.append(os.path.join(folder, file))
        else:
            log('Ignoring "' + fname + '" (not found)', error=True)

    if dedupe:
        return list(OrderedDict.fromkeys(result).keys())

    return result


def try_upload_file(slug, version, current_file, artifact=False):
    """Safely upload a file"""
    try:
        with open(current_file, 'rb') as f:
            folder = os.path.dirname(current_file)
            file = (os.path.basename(current_file), f)
            upload_file(gist_slug=slug, file=file, folder=folder, version=version, artifact=artifact)
    except Exception as e:
        log(str(e), error=True)
