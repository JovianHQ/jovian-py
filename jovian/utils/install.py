"""Utilities to install packages for a cloned gist"""
from __future__ import print_function
import os
import re
import subprocess
from time import sleep
from sys import stderr
from jovian.utils.anaconda import get_conda_bin, CONDA_NOT_FOUND
from jovian.utils.misc import get_platform
from jovian.utils.constants import LINUX, WINDOWS, MACOS, ISSUES_MSG
from jovian.utils.logger import log


YML_PKG_LINE = r'^\s*-\s*([a-zA-Z0-9._-]+)(\s*==?\s*.*)?\s*$'

YML_NAME_LINE = r'^\s*name\s*:\s*([a-zA-Z0-9._-]+)\s*$'


blacklist = [
    'conda',
    'conda-env',
    'attrs'
]


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
    return res[0][0] if len(res) > 0 else None


def extract_env_name(env_fname):
    """Extract the name of the environment from the env file"""
    name = None
    with open(env_fname) as f:
        lines = f.read().split('\n')
        for line in lines:
            res = re.findall(YML_NAME_LINE, line)
            if len(res) > 0:
                name = res[0]
                break
    return name


def write_env_name(env_name, env_fname):
    """Overwrite the environement name into the file"""
    with open(env_fname) as f:
        # Read the environment file
        lines = f.read().split('\n')
        for i, line in enumerate(lines):
            # Check if it matches the name line pattern
            res = re.findall(YML_NAME_LINE, line)
            if len(res) > 0:
                # Extract the name
                name = res[0]
                # Find its poisition in the line
                idx = line.find(name)
                if idx != -1:
                    # Replace the name
                    lines[i] = line[:idx] + env_name + line[idx+len(name):]
    # Save env file with new name
    out_str = '\n'.join(lines)
    with open(env_fname, 'w') as f:
        f.write(out_str)


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
            user_input = input(msg)
        print('')
        # Sanitize the input
        user_input = user_input.strip()
        # Set the final env name
        if user_input:
            env_name = user_input
        if env_name:
            # Write the chosen name to file
            write_env_name(env_name, env_fname)
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


def sanitize_envfile(env_fname, pkgs):
    """Remove the given packages from the environment file"""
    with open(env_fname) as f:
        # Read the lines of the environment file
        lines = f.read().split('\n')
        for i, line in enumerate(lines):
            # Extract package name (if present)
            pkg = extract_pkg(line)
            if pkg and (pkg in pkgs or pkg in blacklist):
                # Comment it out
                lines[i] = "# " + line
    # Save env file with pkgs commented out
    out_str = '\n'.join(lines)
    with open(env_fname, 'w') as f:
        f.write(out_str)


MISSING_MSG = ("WARNING: Some packages listed in the environment definition file could" +
               " not be installed, possibly because the environment was recorded on a different" +
               " operating system. As a result, you have to install some packages manually using " +
               "'conda install <package_name>' if you face errors while executing the code.\n")


def install(env_fname=None, env_name=None):
    """Install packages for a cloned gist"""
    # Check for conda and get the binary path
    conda_bin = get_conda_bin()

    # Identify the right environment file, and exit if absent
    env_fname = identify_env_file(env_fname)
    if env_fname is None:
        log('Failed to detect a conda environment YML file. Skipping..', error=True)
        return
    else:
        log('Detected conda environment file: ' + env_fname + "\n")

    # Get the environment name from user input
    env_name = request_env_name(env_name, env_fname)
    if env_name is None:
        log('Environment name not provided/detected. Skipping..')
        return

    # Construct the command
    command = conda_bin + ' env update --file "' + \
        env_fname + '" --name "' + env_name + '"'

    # Run the command
    log('Executing:\n' + command + "\n")
    install_task = subprocess.Popen(
        command, shell=True, stderr=subprocess.PIPE)

    # Extract the error (if any)
    _, error_str = install_task.communicate()
    error_str = error_str.decode('utf8', errors='ignore')

    if error_str:
        print(error_str, file=stderr)

        # Check for ResolvePackageNotFound error
        notfound, pkgs = check_notfound(error_str)

        # Sanitize the environment file if required
        if notfound:
            log('Installation failed!', error=True)
            log('Ignoring unresolved depedencies and trying again...\n')
            sleep(1)
            sanitize_envfile(env_fname, pkgs)

            # Try to install again
            log('Executing:\n' + command + "\n")
            install_task2 = subprocess.Popen(
                command, shell=True, stderr=subprocess.PIPE)

            # Extract the error (if any)
            _, error_str2 = install_task2.communicate()
            error_str2 = error_str2.decode('utf8', errors='ignore')
            if error_str2:
                print(error_str2, file=stderr)

                # Check for UnsatisfiableError
                unsatisfiable, pkgs2 = check_unsatisfiable(error_str2)

                # Sanitize the environement file further
                if unsatisfiable:
                    log('Installation failed!', error=True)
                    log('Ignoring unsatisfiable depedencies and trying again...\n')
                    sleep(1)
                    sanitize_envfile(env_fname, pkgs2)

                    # Try to install again
                    log('Executing:\n' + command + "\n")
                    install_task3 = subprocess.Popen(
                        command, shell=True, stderr=subprocess.PIPE)

                    # Extract the error (if any)
                    _, error_str3 = install_task3.communicate()
                    error_str3 = error_str3.decode('utf8', errors='ignore')
                    if error_str3:
                        print(error_str3, file=stderr)
                    else:
                        # Display a warning that some packages may be missing
                        log(MISSING_MSG)

    # Print beta warning and github link
    log(ISSUES_MSG)


def activate(env_fname=None):
    """Read the conda environment file and activate the environment"""
    # Check for conda and get the binary path
    try:
        conda_bin = get_conda_bin()
    except:
        log(CONDA_NOT_FOUND, error=True)
        return False

    # Identify the right environment file, and exit if absent
    env_fname = identify_env_file(env_fname)
    if env_fname is None:
        log('Failed to detect a conda environment YML file. Skipping..', error=True)
        return False
    else:
        log('Detected conda environment file: ' + env_fname + "\n")

    # Get the environment name from user input
    env_name = extract_env_name(env_fname)
    if env_name is None:
        log('Environment name not provided/detected. Skipping..')
        return False

    # Activate the environment
    command = conda_bin + " activate " + env_name
    log('Executing:\n' + command + "\n")
    task = subprocess.Popen(
        command, shell=True, stderr=subprocess.PIPE)

    # Extract the error (if any)
    _, error_str = task.communicate()
    error_str = error_str.decode('utf8', errors='ignore')
    print(error_str)

    # TODO: Try again with `source` for older versions of conda
    # Need to check it across platforms

    # Print beta warning and github link
    log(ISSUES_MSG)
