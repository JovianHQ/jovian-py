import os
import re
import yaml
from jovian.utils.constants import LINUX, WINDOWS, MACOS
from jovian.utils.misc import get_platform


YML_PKG_LINE = r'^\s*-\s*([a-zA-Z0-9._-]+)(\s*==?\s*.*)?\s*$'

blacklist = [
    'conda',
    'conda-env',
    'attrs'
]


class Loader(yaml.SafeLoader):
    def __init__(self, stream):
        self._root = os.path.split(stream.name)[0]
        super(Loader, self).__init__(stream)


def get_environment_dict(env_fname):
    """Extract the environment as a python dict"""
    try:
        with open(env_fname, 'r') as stream:
            environment = yaml.load(stream=stream, Loader=Loader)
            return environment
    except yaml.YAMLError as e:
        print("Exception: {} while reading file {}".format(e, env_fname))
        return {}


def dump_environment_to_yaml_file(env_fname, environment):
    """Dump environment into yaml file"""
    try:
        with open(env_fname, 'w') as stream:
            yaml.safe_dump(data=environment, stream=stream, default_style=None,
                           default_flow_style=False)

    except yaml.YAMLError as e:
        print("Exception: {} while accessing file {}".format(e, env_fname))


def write_env_name(env_name, env_fname):
    """Overwrite the environment name into the file"""
    environment = get_environment_dict(env_fname=env_fname)
    if environment and (not environment.get('name') or environment.get('name') != env_name):
        environment['name'] = env_name
        dump_environment_to_yaml_file(env_fname=env_fname, environment=environment)


ENV_NAME_MSG = "Please provide a name for the conda environment"


def request_env_name(env_name, env_fname):
    """Request the user to provide a name for the environment"""
    if env_name is None:
        env_name = extract_env_name(env_fname)
        # Make sure we're not overwriting the base environment
        if env_name == 'base':
            env_name = None
        # Construct the help message with default value
        if env_name:
            msg = ENV_NAME_MSG + " [" + env_name + "]: "
        else:
            msg = ENV_NAME_MSG + ":"
        # Prompt the user for input
        try:
            user_input = raw_input(msg)
        except NameError:
            try:
                user_input = input(msg)
            except EOFError:
                user_input = ''
        print('')
        # Sanitize the input
        user_input = user_input.strip()
        # Set the final env name
        if user_input:
            env_name = user_input
        if env_name:
            # Write the chosen name to file
            write_env_name(env_name, env_fname)
        else:
            env_name = 'base'

    return env_name


def check_notfound(error_str):
    """Check if the error output contains ResolvePackageNotFound"""
    error_lines = error_str.split('\n')
    notfound = False
    pkgs = []
    for line in error_lines:
        if 'ResolvePackageNotFound:' in line:
            notfound = True
        if notfound:
            pkg = extract_pkg(line)
            if pkg:
                pkgs.append(pkg)
    return notfound, pkgs


def check_unsatisfiable(error_str):
    """Check if the error output contains ResolvePackageNotFound"""
    error_lines = error_str.split('\n')
    unsatisfiable = False
    pkgs = []
    for line in error_lines:
        if 'UnsatisfiableError:' in line:
            unsatisfiable = True
        if unsatisfiable:
            pkg = extract_pkg(line)
            if pkg:
                pkgs.append(pkg)
    return unsatisfiable, pkgs


def identify_env_file(env_fname):
    """Find the right conda environment file through trial and errors"""

    if env_fname is None:
        # Look for platform specific environment files (prefer current)
        platforms = [get_platform()] + ["", LINUX, WINDOWS, MACOS]
        for platform in platforms:
            if platform == "":
                expected_fname = 'environment.yml'
            else:
                expected_fname = 'environment-' + platform + '.yml'
            if os.path.exists(expected_fname):
                env_fname = expected_fname
                break

    if env_fname is None:
        # Check for standard environment.yml file
        if os.path.exists('environment.yml'):
            env_fname = 'environment.yml'
    return env_fname


def extract_pkg(line):
    """Extract the name of a package from a YML package line"""
    res = re.findall(YML_PKG_LINE, line)
    return res[0][0]+res[0][1] if len(res) > 0 else None


def extract_env_name(env_fname):
    """Extract the name of the environment from the env file"""
    environment = get_environment_dict(env_fname=env_fname)
    name = environment.get('name') if environment else None
    return name


def remove_packages(dependencies, pkgs):
    new_dependencies = []
    for i, dependency in enumerate(dependencies):
        if isinstance(dependency, str):
            if dependency not in pkgs and dependency not in blacklist:
                new_dependencies.append(dependency)
        elif isinstance(dependency, dict) and dependency.get('pip') and len(dependency['pip']) > 0:
            new_pip_dependencies = remove_packages(dependencies=dependency['pip'], pkgs=pkgs)
            new_dependencies.append({
                'pip': new_pip_dependencies
            })
    return new_dependencies


def sanitize_envfile(env_fname, pkgs):
    """Remove the given packages from the environment file"""
    environment = get_environment_dict(env_fname=env_fname)
    dependencies = environment.get('dependencies')
    dependencies = remove_packages(dependencies=dependencies, pkgs=pkgs)
    environment['dependencies'] = dependencies

    dump_environment_to_yaml_file(env_fname=env_fname, environment=environment)
