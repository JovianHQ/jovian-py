from jovian.utils.error import ApiError, CondaError, ConfigError
import pytest


@pytest.mark.parametrize(
    "Error",
    [
        CondaError,
        ApiError,
        ConfigError
    ]
)
def test_error(Error):
    msg = 'This is a error'
    e = Error(msg)
    assert e.args == (msg,)
