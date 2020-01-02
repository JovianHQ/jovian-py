import os
from unittest import TestCase, mock
from jovian.utils.extension import setup_extension


class TestSetupExtension(TestCase):
    @mock.patch('os.system')
    def test_setup_extension_true(self, mock_system):
        setup_extension(True)
        mock_system.assert_called_with("jupyter nbextension enable jovian_nb_ext/main --sys-prefix")

    @mock.patch('os.system')
    def test_setup_extension_false(self, mock_system):
        setup_extension(False)
        mock_system.assert_called_with("jupyter nbextension disable jovian_nb_ext/main --sys-prefix")
