import os

import click
import yaml

from jovian.utils.constants import LINUX, MACOS, WINDOWS
from jovian.utils.logger import log
from jovian.utils.misc import get_platform

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

    except yaml.YAMLError as e:  # no-cover
        print("Exception: {} while accessing file {}".format(e, env_fname))


def write_env_name(env_name, env_fname):
    """Overwrite the environment name into the file"""
    environment = get_environment_dict(env_fname=env_fname)
    if environment and (not environment.get('name') or environment.get('name') != env_name):
        environment['name'] = env_name
        dump_environment_to_yaml_file(
            env_fname=env_fname, environment=environment)


ENV_NAME_MSG = "Please provide a name for the conda environment"


def request_env_name(env_name, env_fname):
    """Request the user to provide a name for the environment"""
    if env_name is None:
        env_name = extract_env_name(env_fname)
        # Make sure we're not overwriting the base environment
        # Construct the help message with default value
        # Prompt the user for input
        if env_name is None or env_name == 'base':
            user_input = click.prompt(ENV_NAME_MSG, default='base', show_default=False)
        else:
            user_input = click.prompt(ENV_NAME_MSG, default=env_name, show_default=True)

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


MISSING_MSG = ("WARNING: Some packages listed in the environment definition file could" +
               " not be installed, possibly because the environment was recorded on a different" +
               " operating system. As a result, you have to install some packages manually using " +
               "'conda install <package_name>' if you face errors while executing the code.\n")


def check_error(error_str, packages=None):
    """Check if the error output contains ResolvePackageNotFound or UnsatisfiableError"""
    if not packages:
        packages = []
    error_lines = error_str.split('\n')
    error = None
    pkgs = []
    for line in error_lines:
        if 'ResolvePackageNotFound:' in line:
            error = 'unresolved'
        elif 'UnsatisfiableError:' in line:
            error = 'unsatisfiable'
            log(MISSING_MSG)
        if error:
            pkg = extract_package_from_line(line, packages)
            if pkg and pkg not in pkgs:
                pkgs.append(pkg)
    return error, pkgs


def check_pip_failed(error_str):
    """Check if the error output contains Pip failed message"""
    error_lines = error_str.split('\n')
    for line in error_lines:
        if 'Pip failed' in line:
            return True
    return False


def identify_env_file(env_fname, folder_prefix=""):
    """Find the right conda environment file through trial and errors"""

    if env_fname is None:
        # Look for platform specific environment files (prefer current)
        platforms = [get_platform()] + ["", LINUX, WINDOWS, MACOS]
        for platform in platforms:
            if platform == "":
                expected_fname = os.path.join(folder_prefix, 'environment.yml')
            else:
                expected_fname = os.path.join(folder_prefix, 'environment-' + platform + '.yml')

            if os.path.exists(expected_fname):
                env_fname = expected_fname
                break

    return env_fname


def extract_package_from_line(line, packages):
    """Extract the name of a package from an error line"""
    for p in packages:
        if p in line.strip():
            return p
    """if exact version not found in string, look just for package name"""
    for p in packages:
        if '=' in p and p.split('=')[0] in line.strip():
            return p
    return None


def extract_env_name(env_fname):
    """Extract the name of the environment from the env file"""
    environment = get_environment_dict(env_fname=env_fname)
    name = environment.get('name') if environment else None
    return name


def extract_env_packages(env_fname):
    """Extract the (iterable) packages of the environment from the env file
                (including the pip packages in the same list)           """
    environment = get_environment_dict(env_fname=env_fname)
    if not environment:
        return []
    dependencies = environment.get('dependencies')
    return serialize_packages(dependencies=dependencies)


def extract_pip_packages(env_fname):
    """Extract the pip packages of the environment from the env file"""
    environment = get_environment_dict(env_fname=env_fname)
    if not environment:
        return []
    dependencies = environment.get('dependencies')
    if len(dependencies) > 0:
        dependencies[:] = (d for d in dependencies if isinstance(
            d, dict) and d.get('pip'))
    return serialize_packages(dependencies=dependencies)


def serialize_packages(dependencies):
    serialized_dependencies = []
    for i, dependency in enumerate(dependencies):
        if isinstance(dependency, str):
            serialized_dependencies.append(dependency)
        elif isinstance(dependency, dict) and dependency.get('pip') and len(dependency['pip']) > 0:
            for d in dependency['pip']:
                serialized_dependencies.append(d)
    return serialized_dependencies


def remove_packages(dependencies, pkgs):
    new_dependencies = []
    for i, dependency in enumerate(dependencies):
        if isinstance(dependency, str):
            if dependency not in pkgs and dependency not in blacklist:
                new_dependencies.append(dependency)
        elif isinstance(dependency, dict) and dependency.get('pip') and len(dependency['pip']) > 0:
            new_pip_dependencies = remove_packages(
                dependencies=dependency['pip'], pkgs=pkgs)
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
