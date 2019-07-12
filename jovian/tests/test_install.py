import unittest
# import yaml
from jovian.utils.envfile import (check_error, extract_env_name, extract_env_packages,
                                  extract_package_from_line, extract_pip_packages,
                                  get_environment_dict, identify_env_file)

FILES_PREFIX = 'jovian/tests/resources/'     # change based on which dir you're running the tests in
# eg: for running only this file, change FILES_PREFIX = 'resources/'


class InstallUtilsTest(unittest.TestCase):

    def test_identify_env_file(self):
        env_fname = identify_env_file(env_fname=None)
        self.assertEqual(env_fname, 'environment.yml')

    def test_get_environment_dict(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        expected = {'prefix': '/home/admin/anaconda3/envs/test-env',
                    'dependencies': ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                     {'pip': ['six==1.11.0', 'sqlite==2.0.0']}],
                    'channels': ['defaults'], 'name': 'test-env'}
        environment = get_environment_dict(env_fname=env_filename)

        self.assertDictEqual(environment, expected)

        with self.assertRaises(FileNotFoundError):
            get_environment_dict(env_fname='non-existent-file.yml')

        # with self.assertRaises(yaml.YAMLError):    # we're printing the exception, not raising it.
        #     get_environment_dict(env_fname=FILES_PREFIX + 'invalid-yaml-file.yml')

    def test_extract_env_name(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        name = extract_env_name(env_fname=env_filename)
        name2 = extract_env_name(env_fname=FILES_PREFIX+'empty-yaml-file.yml')

        self.assertEqual(name, 'test-env')
        self.assertIsNone(name2)
        with self.assertRaises(FileNotFoundError):
            extract_env_name(env_fname='non-existent-file.yml')

    def test_extract_env_packages(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        dep = extract_env_packages(env_fname=env_filename)
        dep2 = extract_env_packages(env_fname=FILES_PREFIX + 'empty-yaml-file.yml')

        self.assertListEqual(dep, ['mixpanel=1.11.0', 'sigmasix=1.91.0', 'sqlite',
                                   'six==1.11.0', 'sqlite==2.0.0'])
        self.assertListEqual(dep2, [])
        with self.assertRaises(FileNotFoundError):
            extract_env_packages(env_fname='non-existent-file.yml')

    def test_extract_pip_packages(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        env_filename2 = FILES_PREFIX + 'empty-yaml-file.yml'
        dep = extract_pip_packages(env_fname=env_filename)
        dep2 = extract_pip_packages(env_fname=env_filename2)

        self.assertListEqual(dep, ['six==1.11.0', 'sqlite==2.0.0'])
        self.assertListEqual(dep2, [])
        with self.assertRaises(FileNotFoundError):
            extract_env_packages(env_fname='non-existent-file.yml')

    def test_check_error(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        packages = extract_env_packages(env_fname=env_filename)

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

    def test_extract_package_from_line(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        packages = extract_env_packages(env_fname=env_filename)

        lines = [['- mixpanel=1.11.0', 'mixpanel=1.11.0'], ['sqlite<3x not compatible', 'sqlite'],
                 ['', None], ['line containing six < 3.0.x', 'six==1.11.0']]
        for line in lines:
            self.assertEqual(extract_package_from_line(line=line[0], packages=packages), line[1])


if __name__ == '__main__':
    unittest.main()
