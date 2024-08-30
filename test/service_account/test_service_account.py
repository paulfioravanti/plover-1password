import os
import pytest

from plover_1password import service_account


def test_blank_token_env_var_value_on_windows(
    mock_popen_read,
    mocker,
    powershell_command
):
    mock_popen_read(return_value="")
    spy = mocker.spy(os, "popen")

    with pytest.raises(
        ValueError,
        match="No value found for \\$ENV:OP_SERVICE_ACCOUNT_TOKEN"
    ):
        service_account.get_token("Windows", powershell_command)

    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString("
        "$ENV:OP_SERVICE_ACCOUNT_TOKEN)"
    )

def test_blank_token_env_var_value_on_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command
):
    mock_popen_read(return_value="")
    spy = mocker.spy(os, "popen")

    with pytest.raises(
        ValueError,
        match="No value found for \\$OP_SERVICE_ACCOUNT_TOKEN"
    ):
        service_account.get_token("Darwin", bash_command)

    spy.assert_called_once_with(
        "bash -ic 'echo $OP_SERVICE_ACCOUNT_TOKEN'"
    )

def test_get_token_using_windows(
    mock_popen_read,
    mocker,
    powershell_command
):
    mock_popen_read(return_value="windows token")
    spy = mocker.spy(os, "popen")

    assert (
        service_account.get_token("Windows", powershell_command)
        == "windows token"
    )
    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString("
        "$ENV:OP_SERVICE_ACCOUNT_TOKEN)"
    )

def test_get_token_using_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command
):
    mock_popen_read(return_value="mac/linux token")
    spy = mocker.spy(os, "popen")

    assert (
        service_account.get_token("Darwin", bash_command)
        == "mac/linux token"
    )
    spy.assert_called_once_with(
        "bash -ic 'echo $OP_SERVICE_ACCOUNT_TOKEN'"
    )
