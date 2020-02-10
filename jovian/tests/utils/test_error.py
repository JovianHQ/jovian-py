from jovian.utils.error import CondaError, ApiError, ConfigError


def test_conda_error():
    msg = 'This is a error'
    e = CondaError(msg)
    assert e.args == (msg,)


def test_api_error():
    msg = 'This is a error'
    e = ApiError(msg)
    assert e.args == (msg,)


def test_config_error():
    msg = 'This is a error'
    e = ConfigError(msg)
    assert e.args == (msg,)
