import os
import pytest

# NOTE: All the monkeypatching needed for these tests resulted in needing
# to run the tests directly on the token module, rather than the service_account
# interface.
from plover_1password.service_account import token

class MockPopen:
    def __init__(self, return_value):
        self._return_value = return_value

    def read(self):
        return self._return_value

# NOTE: It does not seem to be possible to monkeypatch over an existing
# $OP_SERVICE_ACCOUNT_TOKEN env var, so instead change the name of the env
# var the get_token() function attempts to fetch to be $TOKEN, and then mock
# that value.  This will only then work when calling token.get_token(), and
# not service_account.get_token(), so it's not possible to test from the
# service_account interface.
def test_non_existent_token_var_name_in_env(monkeypatch):
    monkeypatch.setattr(
        token,
        "_TOKEN_ENV_VAR_NAME",
        "MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    )

    with pytest.raises(
        ValueError,
        match="No value found for \\$MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    ):
        token.get_token()

def test_blank_token_env_var_value(monkeypatch):
    monkeypatch.setattr(
        token,
        "_TOKEN_ENV_VAR_NAME",
        "MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    )
    monkeypatch.setenv("OP_SERVICE_ACCOUNT_TOKEN", "")

    with pytest.raises(
        ValueError,
        match="No value found for \\$MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    ):
        token.get_token()

def test_get_token_using_mac_or_linux(monkeypatch, mocker):
    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setattr(
        token,
        "_TOKEN_ENV_VAR_NAME",
        "MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    )
    monkeypatch.setenv("MOCK_OP_SERVICE_ACCOUNT_TOKEN", "mac/linux token")
    monkeypatch.setenv("SHELL", "bash")
    monkeypatch.setattr(
        os,
        "popen",
        lambda _: MockPopen(os.getenv("MOCK_OP_SERVICE_ACCOUNT_TOKEN"))
    )
    spy = mocker.spy(os, "popen")

    assert token.get_token() == "mac/linux token"
    spy.assert_called_once_with(
        "bash -ic 'echo $MOCK_OP_SERVICE_ACCOUNT_TOKEN'"
    )

def test_get_token_using_windows(monkeypatch, mocker):
    monkeypatch.setattr("platform.system", lambda: "Windows")
    monkeypatch.setattr(
        token,
        "_TOKEN_ENV_VAR_NAME",
        "MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    )
    monkeypatch.setenv("MOCK_OP_SERVICE_ACCOUNT_TOKEN", "windows token")
    monkeypatch.setattr(
        os,
        "popen",
        lambda _: MockPopen(os.getenv("MOCK_OP_SERVICE_ACCOUNT_TOKEN"))
    )
    spy = mocker.spy(os, "popen")

    assert token.get_token() == "windows token"
    spy.assert_called_once_with("echo $ENV:MOCK_OP_SERVICE_ACCOUNT_TOKEN")
