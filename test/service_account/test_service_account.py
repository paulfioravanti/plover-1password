import os
import pytest

from plover_1password import service_account

@pytest.fixture()
def patch_op_service_account_token(monkeypatch):
    monkeypatch.setattr(
        "plover_1password.service_account.token._TOKEN_ENV_VAR_NAME",
        "MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    )

    def _method(token_value=None):
        monkeypatch.setenv("MOCK_OP_SERVICE_ACCOUNT_TOKEN", token_value)

    return _method

@pytest.fixture()
def mock_popen_read(mocker):
    mock = mocker.Mock()
    mocker.patch("os.popen", return_value=mock)

    def _method(return_value=None):
        mock.read.return_value = os.getenv(return_value)

    return _method

# NOTE: It does not seem to be possible to monkeypatch over an existing
# $OP_SERVICE_ACCOUNT_TOKEN env var, so instead change the name of the env
# var the get_token() function attempts to fetch to be
# $MOCK_OP_SERVICE_ACCOUNT_TOKEN, and then mock that value.
def test_non_existent_token_var_name_in_env(monkeypatch):
    monkeypatch.setattr(
        "plover_1password.service_account.token._TOKEN_ENV_VAR_NAME",
        "MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    )

    with pytest.raises(
        ValueError,
        match="No value found for \\$MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    ):
        service_account.get_token()

def test_blank_token_env_var_value(patch_op_service_account_token):
    patch_op_service_account_token(token_value="")

    with pytest.raises(
        ValueError,
        match="No value found for \\$MOCK_OP_SERVICE_ACCOUNT_TOKEN"
    ):
        service_account.get_token()

def test_get_token_using_mac_or_linux(
    monkeypatch,
    mocker,
    mock_popen_read,
    patch_op_service_account_token
):
    patch_op_service_account_token(token_value="mac/linux token")
    mock_popen_read(return_value="MOCK_OP_SERVICE_ACCOUNT_TOKEN")

    monkeypatch.setattr("platform.system", lambda: "Darwin")
    monkeypatch.setenv("SHELL", "bash")
    spy = mocker.spy(os, "popen")

    assert service_account.get_token() == "mac/linux token"
    spy.assert_called_once_with(
        "bash -ic 'echo $MOCK_OP_SERVICE_ACCOUNT_TOKEN'"
    )

def test_get_token_using_windows(
    monkeypatch,
    mocker,
    mock_popen_read,
    patch_op_service_account_token,
):
    patch_op_service_account_token(token_value="windows token")
    mock_popen_read(return_value="MOCK_OP_SERVICE_ACCOUNT_TOKEN")

    monkeypatch.setattr("platform.system", lambda: "Windows")
    spy = mocker.spy(os, "popen")

    assert service_account.get_token() == "windows token"
    spy.assert_called_once_with("echo $ENV:MOCK_OP_SERVICE_ACCOUNT_TOKEN")
