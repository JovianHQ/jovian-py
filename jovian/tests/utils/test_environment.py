from unittest import mock, TestCase

from jovian.utils.environment import get_conda_bin, get_conda_env_name, read_conda_env
from jovian.utils.error import CondaError


def mock_os_popen(num=0):
    ret1, ret2 = mock.Mock(), mock.Mock()
    if num == 0:
        ret1.read().strip.return_value = 'usage: conda [-h] [-V] command ...'
        ret2.read().strip.return_value = '/Users/rohitsanjay/miniconda3/bin/conda'
        return ret1, ret2

    elif num == 1:
        ret1.read().strip.return_value = ''
        return ret1, ret1

    elif num == 2:
        ret1.read().strip.return_value = ''
        ret2.read().strip.return_value = '/Users/rohitsanjay/miniconda3/bin/conda'
        return ret1, ret2, ret1

    elif num == 3:
        ret1.read().strip.return_value = 'fake-env'
        return [ret1]

    elif num == 4:
        ret1.read().strip.return_value = ''
        return [ret1]

    elif num == 5:
        ret1.read().strip.return_value = '$CONDA_DEFAULT_ENV'
        return [ret1]

    elif num == 6:
        ret3 = mock.Mock()

        ret1.read().strip.return_value = 'fake-env'  # first call, third call
        ret2.read().strip.return_value = 'conda'  # second call
        ret3.read.return_value = """name: jovian-py-dev
channels:
  - defaults
dependencies:
  - appnope=0.1.0
  - blas=1.0
prefix: /Users/rohitsanjay/miniconda3/envs/jovian-py-dev"""

        return [ret1, ret2, ret1, ret3]

    elif num == 7:
        ret3 = mock.Mock()

        ret1.read().strip.return_value = 'fake-env'  # first call, third call
        ret2.read().strip.return_value = 'conda'  # second call
        ret3.read.return_value = ''

        return [ret1, ret2, ret1, ret3]


class TestGetCondaBin(TestCase):

    @mock.patch("os.popen", side_effect=mock_os_popen())
    def test_get_conda_bin(self, mock_popen):
        assert get_conda_bin() == 'conda'

    @mock.patch("os.popen", side_effect=mock_os_popen(1))
    def test_get_conda_bin_look_for_conda_exe(self, mock_popen):
        assert get_conda_bin() == 'conda'

    @mock.patch("os.popen", side_effect=mock_os_popen(2))
    def test_get_conda_bin_look_for_conda_exe_raises_error(self, mock_popen):
        with self.assertRaises(CondaError):
            get_conda_bin()


class TestGetCondaEnvName(TestCase):

    @mock.patch("os.popen", side_effect=mock_os_popen(3))
    def test_get_conda_env_name(self, mock_popen):
        assert get_conda_env_name() == 'fake-env'

    @mock.patch("os.popen", side_effect=mock_os_popen(4))
    def test_get_conda_env_name_base(self, mock_popen):
        assert get_conda_env_name() == 'base'

    @mock.patch("os.popen", side_effect=mock_os_popen(5))
    def test_get_conda_env_name_echo_conda_default_env(self, mock_popen):
        assert get_conda_env_name() == 'base'


class TestReadCondaEnv(TestCase):

    @mock.patch("os.popen", side_effect=mock_os_popen(6))
    def test_read_conda_env_name_none(self, mock_popen):
        expected_result = """name: jovian-py-dev
channels:
  - defaults
dependencies:
  - appnope=0.1.0
  - blas=1.0
prefix: /Users/rohitsanjay/miniconda3/envs/jovian-py-dev"""
        assert read_conda_env() == expected_result

    @mock.patch("os.popen", side_effect=mock_os_popen(7))
    def test_read_conda_env_empty_env_str_raises_error(self, mock_popen):
        with self.assertRaises(CondaError):
            read_conda_env()
