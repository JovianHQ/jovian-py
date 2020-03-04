import os
from unittest import TestCase, mock
from unittest.mock import ANY

from jovian.utils.install import run_command, install, activate


class EnvFile(TestCase):
    def setUp(self):
        os.chdir('jovian/tests/resources/yaml')

    def tearDown(self):
        os.chdir('../' * 4)


class TestRunCommand(EnvFile):

    @mock.patch("subprocess.Popen")
    def test_run_command(self, mock_popen):
        mock_popen().communicate.return_value = (None, b'')
        run_command('conda env list', 'environment-test.yml', ['mixpanel=1.11.0', 'sigmasix=1.91.0'])

        mock_popen.assert_called_with('conda env list', shell=True, stderr=ANY)
