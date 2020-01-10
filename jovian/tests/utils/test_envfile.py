import os
import yaml
from unittest import TestCase, mock
from jovian.utils.envfile import (check_error, extract_env_name, extract_env_packages, extract_package_from_line,
                                  extract_pip_packages, get_environment_dict, identify_env_file,
                                  dump_environment_to_yaml_file, write_env_name, remove_packages,
                                  sanitize_envfile, serialize_packages, request_env_name, check_pip_failed)


class EnvFile(TestCase):
    def setUp(self):
        os.chdir('jovian/tests/resources/yaml')

    def tearDown(self):
        os.chdir('../' * 4)


class TestIdentityEnvFile(EnvFile):

    def test_identify_env_file_no_environment_file(self):
        self.assertIsNone(identify_env_file(env_fname=None))

    def test_identify_env_file_exists(self):
        os.system('touch environment.yml')

        self.assertEqual(identify_env_file(env_fname=None), 'environment.yml')

        os.system('rm environment.yml')


class TestGetEnvironmentDict(EnvFile):
    def test_get_environment_dict(self):
        expected_result = {'prefix': '/home/admin/anaconda3/envs/test-env',
                           'dependencies': ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                            {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                           'channels': ['defaults'], 'name': 'test-env'}
        environment = get_environment_dict(env_fname='environment-test.yml')

        self.assertDictEqual(environment, expected_result)

    def test_get_environment_dict_non_existent_file(self):
        expected = {'prefix': '/home/admin/anaconda3/envs/test-env',
                    'dependencies': ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                     {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                    'channels': ['defaults'], 'name': 'test-env'}
        environment = get_environment_dict(env_fname='environment-test.yml')

        with self.assertRaises(FileNotFoundError):
            get_environment_dict(env_fname='non-existent-file.yml')

    def test_get_environment_dict_raises_exception_invalid_file(self):
        expected_result = {}

        self.assertDictEqual(get_environment_dict('invalid-yaml-file.yml'), expected_result)


class TestExtractEnvName(EnvFile):
    def test_extract_env_name(self):
        name = extract_env_name(env_fname='environment-test.yml')
        name2 = extract_env_name(env_fname='empty-yaml-file.yml')

        self.assertEqual(name, 'test-env')
        self.assertIsNone(name2)
        with self.assertRaises(FileNotFoundError):
            extract_env_name(env_fname='non-existent-file.yml')


class TestExtractEnvPackages(EnvFile):
    def test_extract_env_packages(self):

        dep = extract_env_packages(env_fname='environment-test.yml')
        dep2 = extract_env_packages(env_fname='empty-yaml-file.yml')

        self.assertListEqual(dep, ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                   'six==1.11.0', 'sqlite==2.0.0'])
        self.assertListEqual(dep2, [])
        with self.assertRaises(FileNotFoundError):
            extract_env_packages(env_fname='non-existent-file.yml')


class TestExtractPipPackages(EnvFile):
    def test_extract_pip_packages(self):
        dep = extract_pip_packages(env_fname='environment-test.yml')
        dep2 = extract_pip_packages(env_fname='empty-yaml-file.yml')

        self.assertListEqual(dep, ['six==1.11.0', 'sqlite==2.0.0'])
        self.assertListEqual(dep2, [])
        with self.assertRaises(FileNotFoundError):
            extract_env_packages(env_fname='non-existent-file.yml')


class TestCheckError(EnvFile):
    def test_check_error(self):

        packages = extract_env_packages(env_fname='environment-test.yml')

        error_str = '''ResolvePackageNotFound: 
                        - mixpanel=1.11.0'''
        error_str2 = '''UnsatisfiableError: 
                                - sigmasix=1.91.0'''
        error_str3 = '''AnyOtherException: 
                                - sigmasix=1.91.0'''
        error, pkgs = check_error(error_str=error_str, packages=packages)
        error2, pkgs2 = check_error(error_str=error_str2, packages=packages)
        error3, pkgs3 = check_error(error_str=error_str3, packages=packages)

        self.assertEqual(error, 'unresolved')
        self.assertListEqual(pkgs, ['mixpanel=1.11.0'])
        self.assertEqual(error2, 'unsatisfiable')
        self.assertListEqual(pkgs2, ['sigmasix=1.91.0'])
        self.assertIsNone(error3)
        self.assertListEqual(pkgs3, [])

    def test_check_error_no_packages(self):
        error_str = '''ResolvePackageNotFound: 
                        - mixpanel=1.11.0'''
        packages = []
        error, pkgs = check_error(error_str=error_str, packages=packages)

        self.assertEqual(error, 'unresolved')
        self.assertListEqual(pkgs, [])


class TestExtractPackageFromLine(EnvFile):
    def test_extract_package_from_line(self):
        packages = extract_env_packages(env_fname='environment-test.yml')

        lines = [['- mixpanel=1.11.0', 'mixpanel=1.11.0'], ['sqlite<3x not compatible', 'sqlite'],
                 ['', None], ['line containing six < 3.0.x', 'six==1.11.0']]
        for line in lines:
            self.assertEqual(extract_package_from_line(line=line[0], packages=packages), line[1])


class TestDumpEnvironmentToYamlFile(EnvFile):
    data = {'channels': ['defaults'],
            'dependencies': ['mixpanel=1.11.0',
                             'sigmasix=1.91.0',
                             'sqlite',
                             {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
            'name': 'test-env',
            'prefix': '/home/admin/anaconda3/envs/test-env'}

    def setUp(self):
        super().setUp()
        dump_environment_to_yaml_file('test.yml', self.data)

    def test_dump_environment_to_yaml_file_normal(self):
        self.assertEqual(get_environment_dict('test.yml'), self.data)

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


class TestRemovePackages(EnvFile):

    def test_remove_packages(self):
        packages = extract_env_packages(env_fname='environment-test.yml')
        dependencies = ['dep1', 'dep2', 'mixpanel=1.11.0', 'sqlite']

        expected_result = ['dep1', 'dep2']

        self.assertEqual(remove_packages(dependencies, packages), expected_result)

    def test_remove_packages_pip(self):
        packages = extract_env_packages(env_fname='environment-test.yml')
        dependencies = ['dep1', 'mixpanel=1.11.0', {'pip': ['six==1.11.0', 'dep3']}]

        expected_result = ['dep1', {'pip': ['dep3']}]

        self.assertEqual(remove_packages(dependencies, packages), expected_result)


class TestSanitizeEnvfile(EnvFile):
    data = {'channels': ['defaults'],
            'dependencies': ['mixpanel=1.11.0',
                             'sigmasix=1.91.0',
                             'sqlite',
                             {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
            'name': 'test-env',
            'prefix': '/home/admin/anaconda3/envs/test-env'}

    def setUp(self):
        super().setUp()
        dump_environment_to_yaml_file('test.yml', self.data)

    def test_sanitize_envfile(self):
        packages = ['six==1.11.0', 'sigmasix=1.91.0']
        sanitize_envfile('test.yml', packages)

        expected_result = {'channels': ['defaults'],
                           'dependencies': ['mixpanel=1.11.0',
                                            'sqlite',
                                            {'pip': ['sqlite==2.0.0']}],
                           'name': 'test-env',
                           'prefix': '/home/admin/anaconda3/envs/test-env'}
        self.assertEqual(get_environment_dict('test.yml'), expected_result)

    def tearDown(self):
        os.system('rm test.yml')
        super().tearDown()


class TestSerializePackages(EnvFile):

    def test_serialize_packages(self):
        dependencies = ['dep1', 'mixpanel=1.11.0', {'pip': ['six==1.11.0', 'dep3']}]

        expected_result = ['dep1', 'mixpanel=1.11.0', 'six==1.11.0', 'dep3']

        self.assertEqual(serialize_packages(dependencies), expected_result)


class TestRequestEnvName(EnvFile):
    def tearDown(self):
        write_env_name('test-env', 'environment-test.yml')
        super().tearDown()

    @mock.patch("jovian.utils.envfile.click.prompt", return_value="")
    def test_request_env_name(self, mock_prompt):
        expected_result = 'test-env'

        self.assertEqual(request_env_name(env_name=None, env_fname='environment-test.yml'), expected_result)

    @mock.patch("jovian.utils.envfile.click.prompt", return_value="test-env-changed")
    def test_request_env_name_changed(self, mock_prompt):
        expected_result = 'test-env-changed'

        self.assertEqual(request_env_name(env_name=None, env_fname='environment-test.yml'), expected_result)

    @mock.patch("jovian.utils.envfile.extract_env_name", return_value=None)
    @mock.patch("jovian.utils.envfile.click.prompt", return_value="test-env-changed")
    def test_request_env_name_no_env_name(self, mock_prompt, mock_extract_env_name):
        expected_result = 'test-env-changed'

        self.assertEqual(request_env_name(env_name=None, env_fname='environment-test.yml'), expected_result)

    @mock.patch("jovian.utils.envfile.extract_env_name", return_value=None)
    @mock.patch("jovian.utils.envfile.click.prompt", return_value="")
    def test_request_env_name_no_env_name_default_to_base(self, mock_prompt, mock_extract_env_name):
        expected_result = 'base'

        self.assertEqual(request_env_name(env_name=None, env_fname='environment-test.yml'), expected_result)


class TestCheckPipFailed(TestCase):
    def test_check_pip_failed_true(self):
        error_str = '''Could not install
                       Pip failed with error code 2'''

        self.assertTrue(check_pip_failed(error_str))

    def test_check_pip_failed_false(self):
        error_str = '''Pip successfully installed package'''

        self.assertFalse(check_pip_failed(error_str))
