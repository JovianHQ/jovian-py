"""Utilities to install packages for a cloned gist"""
from __future__ import print_function
import os
import re
import subprocess
from sys import stderr
from jovian.utils.anaconda import get_conda_bin
from jovian.utils.misc import get_platform
from jovian.utils.constants import LINUX, WINDOWS, MACOS
from jovian.utils.logger import log


YML_PKG_LINE = r'^\s*-\s*([a-zA-Z0-9._-]+)(\s*==?\s*.*)?\s*$'

YML_NAME_LINE = r'^\s*name\s*:\s*([a-zA-Z0-9._-]+)\s*$'


def identify_env_file(env_fname):
    """Find the right conda environment file through trial and errors"""
    if env_fname is None:
        # Look for platform specific environment files (prefer current)
        platforms = [get_platform()] + [LINUX, WINDOWS, MACOS]
        for platform in platforms:
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


ENV_NAME_MSG = "Please provide a name for the conda environment "


def request_env_name(env_name, env_fname):
    """Request the user to provide a name for the environment"""
    if env_name is None:
        env_name = extract_env_name(env_fname)
        msg = ENV_NAME_MSG + "(" + env_name + "): "
        try:
            user_input = raw_input(msg)
        except NameError:
            user_input = input(msg)
        user_input = user_input.strip()
        if user_input:
            env_name = user_input
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


def sanitize_envfile(env_fname, pkgs):
    """Remove the given packages from the environment file"""
    with open(env_fname) as f:
        # Read the lines of the environment file
        lines = f.read().split('\n')
        for i, line in enumerate(lines):
            # Extract package name (if present)
            pkg = extract_pkg(line)
            if pkg and pkg in pkgs:
                # Comment it out
                lines[i] = "# " + line
    # Save env file with pkgs commented out
    out_str = '\n'.join(lines)
    with open(env_fname, 'w') as f:
        f.write(out_str)


def install(env_fname=None, env_name=None):
    """Install packages for a cloned gist"""
    # Check for conda and get the binary path
    conda_bin = get_conda_bin()

    # Identify the right environment file, and exit if absent
    env_fname = identify_env_file(env_fname)
    if env_fname is None:
        log('Failed to detect a conda environment YML file. Skipping..', error=True)
    else:
        log('Detected conda environment file: ' + env_fname + "\n")

    # Get the environment name from user input
    env_name = request_env_name(env_name, env_fname)

    # Construct the command
    command = conda_bin + ' env update --file "' + \
        env_fname + '" --name "' + env_name + '"'

    # Run the command
    log('Executing:\n' + command + "\n")
    install_task = subprocess.Popen(
        command, shell=True, stderr=subprocess.PIPE)

    # Extract the error (if any)
    _, error_str = install_task.communicate()
    if error_str:
        # Display the error
        log('Installation failed!', error=True)
        print(error_str, file=stderr)

        # Check for ResolvePackageNotFound error
        notfound, pkgs = check_notfound(error_str)

        # Sanitize the environment file if required
        if notfound:
            log('Ignoring unresolved depedencies and trying again\n')
            sanitize_envfile(env_fname, pkgs)

            # Try to install again
            log('Executing:\n' + command + "\n")
            install_task2 = subprocess.Popen(
                command, shell=True, stderr=subprocess.PIPE)

            # Extract the error (if any)
            _, error_str2 = install_task2.communicate()
            if error_str2:
                # Display the error
                log('Installation failed!', error=True)
                print(error_str2, file=stderr)
            else:
                # Return success
                return True
    # Return failure
    return False
