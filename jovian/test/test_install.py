import unittest
# import yaml
from jovian.utils.envfile import (check_notfound, check_unsatisfiable, extract_env_name,
                                  extract_pkg, get_environment_dict, identify_env_file)

FILES_PREFIX = 'jovian/test/resources/'     # change based on which dir you're running the tests in
# eg: for running only this file, change FILES_PREFIX = 'resources/'


class InstallUtilsTest(unittest.TestCase):

    def test_identify_env_file(self):
        env_fname = identify_env_file(env_fname=None)
        self.assertEqual(env_fname, 'environment.yml')

    def test_get_environment_dict(self):
        env_filename = FILES_PREFIX + 'environment.yml'
        expected = {'prefix': '/home/admin/anaconda3/envs/test-env', 'dependencies':
            ['six=1.11.0', 'sqlite'], 'channels': ['defaults'], 'name': 'test-env'}
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
        with self.assertRaises(FileNotFoundError):    # we're printing error, not raising it.
            extract_env_name(env_fname='non-existent-file.yml')

    def test_check_notfound(self):
        error_str = '''ResolvePackageNotFound: 
                        - sixx=1.11.0'''
        error_str2 = '''UnsatisfiableError: 
                                - six=1.91.0'''
        notfound, pkgs = check_notfound(error_str)
        notfound2, pkgs2 = check_notfound(error_str2)

        self.assertTrue(notfound)
        self.assertListEqual(pkgs, ['sixx=1.11.0'])
        self.assertFalse(notfound2)
        self.assertListEqual(pkgs2, [])

    def test_unsatisfiable(self):
        error_str = '''UnsatisfiableError: 
                        - six=1.91.0'''

        error_str2 = '''AnyOtherException: 
                        - six=1.91.0'''
        unsatisfiable, pkgs = check_unsatisfiable(error_str)
        unsatisfiable2, pkgs2 = check_unsatisfiable(error_str2)

        self.assertTrue(unsatisfiable)
        self.assertListEqual(pkgs, ['six=1.91.0'])
        self.assertFalse(unsatisfiable2, False)
        self.assertListEqual(pkgs2, [])

    def test_extract_pkg(self):
        lines = [['- six=1.11.0', 'six=1.11.0'], ['sqlite', None], ['', None], ['- six=1.11.0',
                                                                                'six=1.11.0']]
        for line in lines:
            self.assertEqual(extract_pkg(line=line[0]), line[1])


if __name__ == '__main__':
    unittest.main()
