import pytest
import subprocess

from plover_1password import service_account


def test_blank_token_env_var_value_on_windows(
    mock_subprocess_run,
    mocker,
    powershell_command
):
    mock_subprocess_run(return_value="")
    spy = mocker.spy(subprocess, "run")

    with pytest.raises(
        ValueError,
        match="No value found for \\$ENV:OP_SERVICE_ACCOUNT_TOKEN"
    ):
        service_account.get_token("Windows", powershell_command)

    spy.assert_called_once_with(
        "powershell -command "
        "\"$ExecutionContext.InvokeCommand.ExpandString("
        "$ENV:OP_SERVICE_ACCOUNT_TOKEN)\"",
        capture_output=True,
        check=False,
        encoding="utf-8",
        shell=True
    )

def test_blank_token_env_var_value_on_mac_or_linux(
    mock_subprocess_run,
    mocker,
    bash_command
):
    mock_subprocess_run(return_value="")
    spy = mocker.spy(subprocess, "run")

    with pytest.raises(
        ValueError,
        match="No value found for \\$OP_SERVICE_ACCOUNT_TOKEN"
    ):
        service_account.get_token("Darwin", bash_command)

    spy.assert_called_once_with(
        "bash -ic 'echo $OP_SERVICE_ACCOUNT_TOKEN'",
        capture_output=True,
        check=False,
        encoding="utf-8",
        shell=True
    )

def test_get_token_using_windows(
    mock_subprocess_run,
    mocker,
    powershell_command
):
    mock_subprocess_run(return_value="windows token")
    spy = mocker.spy(subprocess, "run")

    assert (
        service_account.get_token("Windows", powershell_command)
        == "windows token"
    )
    spy.assert_called_once_with(
        "powershell -command "
        "\"$ExecutionContext.InvokeCommand.ExpandString("
        "$ENV:OP_SERVICE_ACCOUNT_TOKEN)\"",
        capture_output=True,
        check=False,
        encoding="utf-8",
        shell=True
    )

def test_get_token_using_mac_or_linux(
    mock_subprocess_run,
    mocker,
    bash_command
):
    mock_subprocess_run(return_value="mac/linux token")
    spy = mocker.spy(subprocess, "run")

    assert (
        service_account.get_token("Darwin", bash_command)
        == "mac/linux token"
    )
    spy.assert_called_once_with(
        "bash -ic 'echo $OP_SERVICE_ACCOUNT_TOKEN'",
        capture_output=True,
        check=False,
        encoding="utf-8",
        shell=True
    )
