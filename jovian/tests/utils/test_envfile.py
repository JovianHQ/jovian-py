import os
from unittest import TestCase, mock
from textwrap import dedent

import yaml
import pytest

from jovian.utils.envfile import (check_error, check_pip_failed, dump_environment_to_yaml_file, extract_env_name,
                                  extract_env_packages, extract_package_from_line, extract_pip_packages,
                                  get_environment_dict, identify_env_file, remove_packages, request_env_name,
                                  sanitize_envfile, serialize_packages, write_env_name)
from jovian.tests.resources.shared import temp_directory, fake_envfile


def test_identify_env_file_no_environment_file():
    with temp_directory():
        assert identify_env_file(env_fname=None) == None


def test_identify_env_file_exists():
    with fake_envfile():
        assert identify_env_file(env_fname=None) == 'environment.yml'


def test_get_environment_dict():
    with fake_envfile():
        expected_result = {'prefix': '/home/admin/anaconda3/envs/test-env',
                           'dependencies': ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                            {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                           'channels': ['defaults'], 'name': 'test-env'}
        environment = get_environment_dict(env_fname='environment.yml')

        assert environment == expected_result


def test_get_environment_dict_non_existent_file():
    with fake_envfile():
        expected = {'prefix': '/home/admin/anaconda3/envs/test-env',
                    'dependencies': ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                     {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                    'channels': ['defaults'], 'name': 'test-env'}
        environment = get_environment_dict(env_fname='environment.yml')

        with pytest.raises(FileNotFoundError):
            get_environment_dict(env_fname='non-existent-file.yml')


def test_get_environment_dict_raises_exception_invalid_file():
    with fake_envfile():
        with open('invalid-yaml-file.yml', 'w') as f:
            f.write(dedent("""
            ok:
                sub1: sub1
                ][
            hello:
                world: world
                some: other
            """))
        assert get_environment_dict('invalid-yaml-file.yml') == {}


@pytest.mark.parametrize(
    "func, env_fname, expected_result",
    [
        (extract_env_name, 'environment.yml', 'test-env'),
        (extract_env_name, 'empty-yaml-file.yml', None),
        (extract_env_packages, 'environment.yml', ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                                   'six==1.11.0', 'sqlite==2.0.0']),
        (extract_env_packages, 'empty-yaml-file.yml', []),
        (extract_pip_packages, 'environment.yml', ['six==1.11.0', 'sqlite==2.0.0']),
        (extract_pip_packages, 'empty-yaml-file.yml', []),
    ]
)
def test_extract(func, env_fname, expected_result):
    with fake_envfile():
        assert func(env_fname) == expected_result

        with pytest.raises(FileNotFoundError):
            func('non-existent-file.yml')


@pytest.mark.parametrize(
    "error_str, expected_result",
    [
        (
            '''ResolvePackageNotFound:
                    - mixpanel=1.11.0''',
            ('unresolved', ['mixpanel=1.11.0'])
        ),
        (
            '''UnsatisfiableError:
                            - sigmasix=1.91.0''',
            ('unsatisfiable', ['sigmasix=1.91.0'])
        ),
        (
            '''AnyOtherException:
                            - sigmasix=1.91.0''',
            (None, [])
        ),
    ]
)
def test_check_error(error_str, expected_result):
    with fake_envfile():
        packages = extract_env_packages(env_fname='environment.yml')
        assert check_error(error_str=error_str, packages=packages) == expected_result


def test_check_error_no_packages():
    error_str = '''ResolvePackageNotFound:
                    - mixpanel=1.11.0'''
    packages = []
    assert check_error(error_str=error_str, packages=[]) == ('unresolved', [])


@pytest.mark.parametrize(
    "line, expected_result",
    [
        ('- mixpanel=1.11.0', 'mixpanel=1.11.0'),
        ('sqlite<3x not compatible', 'sqlite'),
        ('', None),
        ('line containing six < 3.0.x', 'six==1.11.0'),
    ]
)
def test_extract_package_from_line(line, expected_result):
    with fake_envfile():
        packages = extract_env_packages(env_fname='environment.yml')
        assert extract_package_from_line(line=line, packages=packages) == expected_result


def test_dump_environment_to_yaml_file_normal():
    with fake_envfile():
        data = {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0',
                                 'sigmasix=1.91.0',
                                 'sqlite',
                                 {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                'name': 'test-env',
                'prefix': '/home/admin/anaconda3/envs/test-env'}
        dump_environment_to_yaml_file('test.yml', data)

        assert get_environment_dict('test.yml') == data


@pytest.mark.parametrize(
    "data, name",
    [
        (
            {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0'],
                'name': 'test-env',
                'prefix': '/home/admin/anaconda3/envs/test-env'},
            'test-env-changed'
        ),
        (
            {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0'],
                'prefix': '/home/admin/anaconda3/envs/test-env'},
            'test-env'
        ),
        (
            {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0'],
                'name': 'test-env',
                'prefix': '/home/admin/anaconda3/envs/test-env'},
            'test-env'
        ),
    ]
)
def test_write_env_name(data, name):
    with fake_envfile():
        dump_environment_to_yaml_file('test.yml', data)

        write_env_name(name, 'test.yml')

        assert get_environment_dict('test.yml')['name'] == name


@pytest.mark.parametrize(
    "dependencies, expected_result",
    [
        (['dep1', 'dep2', 'mixpanel=1.11.0', 'sqlite'], ['dep1', 'dep2']),
        (['dep1', 'mixpanel=1.11.0', {'pip': ['six==1.11.0', 'dep3']}], ['dep1', {'pip': ['dep3']}]),
    ]
)
def test_remove_packages(dependencies, expected_result):
    with fake_envfile():
        packages = extract_env_packages(env_fname='environment.yml')
        assert remove_packages(dependencies, packages) == expected_result


def test_sanitize_envfile():
    with fake_envfile():
        packages = ['six==1.11.0', 'sigmasix=1.91.0']
        sanitize_envfile('environment.yml', packages)

        expected_result = {'channels': ['defaults'],
                           'dependencies': ['mixpanel=1.11.0',
                                            'sqlite',
                                            {'pip': ['sqlite==2.0.0']}],
                           'name': 'test-env',
                           'prefix': '/home/admin/anaconda3/envs/test-env'}

        assert get_environment_dict('environment.yml') == expected_result


@pytest.mark.parametrize(
    "dependencies, expected_result",
    [
        (
            ['dep1', 'mixpanel=1.11.0', {'pip': None}],
            ['dep1', 'mixpanel=1.11.0']
        ),
        (
            ['dep1', 'mixpanel=1.11.0', {'pip': ['six==1.11.0', 'dep3']}],
            ['dep1', 'mixpanel=1.11.0', 'six==1.11.0', 'dep3']
        ),
        (
            ['dep1', 'mixpanel=1.11.0', 'sigmasix=1.91.0', {'pip': ['six==1.11.0', 'dep3']}],
            ['dep1', 'mixpanel=1.11.0', 'sigmasix=1.91.0', 'six==1.11.0', 'dep3']
        ),
    ]
)
def test_serialize_packages(dependencies, expected_result):
    assert serialize_packages(dependencies) == expected_result


@pytest.mark.parametrize(
    "prompt_ret_val, extract_env_name_ret_val, expected_result",
    [
        (
            "",
            "test-env",
            "test-env",
        ),
        (
            "test-env-changed",
            "test-env",
            "test-env-changed",
        ),
        (
            "test-env-changed",
            None,
            "test-env-changed",
        ),
        (
            "",
            None,
            "base",
        ),
    ]
)
def test_request_env_name(prompt_ret_val, extract_env_name_ret_val, expected_result):
    with fake_envfile():
        with mock.patch("jovian.utils.envfile.click.prompt", return_value=prompt_ret_val), \
                mock.patch("jovian.utils.envfile.extract_env_name", return_value=extract_env_name_ret_val):
            assert request_env_name(env_name=None, env_fname='environment.yml') == expected_result


@pytest.mark.parametrize(
    "error_str, expected_result",
    [
        ('''Could not install
                    Pip failed with error code 2''', True),
        ('''Pip successfully installed package''', False),
    ]
)
def test_check_pip_failed(error_str, expected_result):
    assert check_pip_failed(error_str) == expected_result
