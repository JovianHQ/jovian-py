"""Utilities to install packages for a cloned gist"""
from __future__ import print_function
import subprocess
from time import sleep
from sys import stderr
from jovian.utils.anaconda import get_conda_bin, CONDA_NOT_FOUND
from jovian.utils.constants import ISSUES_MSG
from jovian.utils.logger import log
from jovian.utils.envfile import (check_notfound, check_unsatisfiable, extract_env_name,
                                  identify_env_file, request_env_name, sanitize_envfile)


MISSING_MSG = ("WARNING: Some packages listed in the environment definition file could" +
               " not be installed, possibly because the environment was recorded on a different" +
               " operating system. As a result, you have to install some packages manually using " +
               "'conda install <package_name>' if you face errors while executing the code.\n")


def install(env_fname=None, env_name=None):
    """Install packages for a cloned gist"""
    # Check for conda and get the binary path
    conda_bin = get_conda_bin()

    # Identify the right environment file, and exit if absent
    env_fname = identify_env_file(env_fname=env_fname)
    if env_fname is None:
        log('Failed to detect a conda environment YML file. Skipping..', error=True)
        return
    else:
        log('Detected conda environment file: ' + env_fname + "\n")

    # Get the environment name from user input
    env_name = request_env_name(env_name=env_name, env_fname=env_fname)
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
            log('Ignoring unresolved dependencies and trying again...\n')
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

                # Sanitize the environment file further
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
    env_fname = identify_env_file(env_fname=env_fname)
    if env_fname is None:
        log('Failed to detect a conda environment YML file. Skipping..', error=True)
        return False
    else:
        log('Detected conda environment file: ' + env_fname + "\n")

    # Get the environment name from user input
    env_name = extract_env_name(env_fname=env_fname)
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
