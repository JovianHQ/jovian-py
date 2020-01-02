from jovian.utils.logger import log


def test_log(capsys):
    log("This is a log")
    captured = capsys.readouterr()
    assert captured.out.strip() == "[jovian] This is a log"


def test_log_error(capsys):
    log("This is an error", error=True)
    captured = capsys.readouterr()
    assert captured.err.strip() == "[jovian] Error: This is an error"
