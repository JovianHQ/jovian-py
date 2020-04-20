import os
from unittest import TestCase, mock

import pytest

from jovian.utils.extension import setup_extension


@pytest.mark.parametrize(
    "enable, expected_result",
    [
        (True, "jupyter nbextension enable jovian_nb_ext/main --sys-prefix"),
        (False, "jupyter nbextension disable jovian_nb_ext/main --sys-prefix"),
    ]
)
@mock.patch('os.system')
def test_setup_extension_true(mock_system, enable, expected_result):
    setup_extension(enable=enable)
    mock_system.assert_called_with(expected_result)
