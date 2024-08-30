import os
import pytest

from plover_1password import secret_reference


def test_no_env_vars_in_secret_reference(bash_command):
    assert(
        secret_reference.expand_env_vars(
            bash_command,
            "op://Plover/Personal/Phone/Mobile"
        ) == "op://Plover/Personal/Phone/Mobile"
    )

def test_expand_secret_reference_using_mac_or_linux(
    mock_popen_read,
    mocker,
    bash_command
):
    mock_popen_read(return_value="op://Plover/Personal/Phone/Mobile")
    spy = mocker.spy(os, "popen")

    assert(
        secret_reference.expand_env_vars(
            bash_command,
            "op://$VAULT_NAME/$ITEM_NAME/$SECTION_NAME/Mobile"
        ) == "op://Plover/Personal/Phone/Mobile"
    )
    spy.assert_called_once_with(
        "bash -ic 'echo op://$VAULT_NAME/$ITEM_NAME/$SECTION_NAME/Mobile'"
    )

def test_expand_secret_reference_using_windows(
    mock_popen_read,
    mocker,
    powershell_command
):
    mock_popen_read(return_value="op://Plover/Personal/Phone/Mobile")
    spy = mocker.spy(os, "popen")

    assert (
        secret_reference.expand_env_vars(
            powershell_command,
            "op://$ENV:VAULT_NAME/$ENV:ITEM_NAME/$ENV:SECTION_NAME/Mobile"
        )
    ) == "op://Plover/Personal/Phone/Mobile"
    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString("
        "op://$ENV:VAULT_NAME/$ENV:ITEM_NAME/$ENV:SECTION_NAME/Mobile)"
    )
