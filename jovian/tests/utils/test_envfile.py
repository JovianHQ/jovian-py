import os
import sys

from unittest import TestCase, mock
from jovian.utils.envfile import get_environment_dict, dump_environment_to_yaml_file, write_env_name, request_env_name


class EnvFile(TestCase):
    def setUp(self):
        os.chdir('jovian/tests/resources/yaml')

    def tearDown(self):
        os.chdir('../' * 4)


class TestGetEnvironmentDict(EnvFile):

    def test_get_environment_dict(self):
        expected_result = {'channels': ['defaults'],
                           'dependencies': ['mixpanel=1.11.0',
                                            'sigmasix=1.91.0',
                                            'sqlite',
                                            {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                           'name': 'test-env',
                           'prefix': '/home/admin/anaconda3/envs/test-env'}

        self.assertEqual(get_environment_dict('environment.yml'), expected_result)

    def test_get_environment_dict_invalid_yml(self):
        expected_result = {}

        self.assertEqual(get_environment_dict('invalid-yaml-file.yml'), expected_result)

    def test_get_environment_dict_raises_exception_invalid_file(self):
        expected_result = {}

        self.assertEqual(get_environment_dict('invalid-yaml-file.yml'), expected_result)

    def test_get_environment_dict_raises_exception_non_existent_file(self):
        with self.assertRaises(FileNotFoundError):
            get_environment_dict('non-existent-file.yml')

    def test_get_environment_dict_raises_exception_empty_file(self):
        expected_result = None

        self.assertEqual(get_environment_dict('empty-yaml-file.yml'), expected_result)


class TestDumpEnvironmentToYamlFile(EnvFile):
    def test_dump_environment_to_yaml_file_normal(self):
        data = {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0',
                                 'sigmasix=1.91.0',
                                 'sqlite',
                                 {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                'name': 'test-env',
                'prefix': '/home/admin/anaconda3/envs/test-env'}
        dump_environment_to_yaml_file('test.yml', data)

        self.assertEqual(get_environment_dict('test.yml'), data)

    def tearDown(self):
        os.system('rm test.yml')
        super().tearDown()


class TestWriteEnvName(EnvFile):

    def test_write_env_name_new_name(self):
        data = {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0'],
                'name': 'test-env',
                'prefix': '/home/admin/anaconda3/envs/test-env'}
        dump_environment_to_yaml_file('test.yml', data)

        write_env_name('test-env-changed', 'test.yml')

        expected_result = 'test-env-changed'
        self.assertEqual(get_environment_dict('test.yml')['name'], expected_result)

    def test_write_env_name_no_name(self):
        data = {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0'],
                'prefix': '/home/admin/anaconda3/envs/test-env'}
        dump_environment_to_yaml_file('test.yml', data)

        write_env_name('test-env', 'test.yml')

        expected_result = 'test-env'
        self.assertEqual(get_environment_dict('test.yml')['name'], expected_result)

    def test_write_env_name_same_name(self):
        data = {'channels': ['defaults'],
                'dependencies': ['mixpanel=1.11.0'],
                'name': 'test-env',
                'prefix': '/home/admin/anaconda3/envs/test-env'}
        dump_environment_to_yaml_file('test.yml', data)

        write_env_name('test-env', 'test.yml')

        expected_result = 'test-env'
        self.assertEqual(get_environment_dict('test.yml')['name'], expected_result)

    def tearDown(self):
        os.system('rm test.yml')
        super().tearDown()
