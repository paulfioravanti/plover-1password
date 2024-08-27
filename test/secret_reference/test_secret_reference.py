import os
import pytest

from plover_1password import secret_reference


# NOTE: Given that the command passed in to `os.popen` will be different
# between Windows and non-Windows:
#
# `echo $ExecutionContext.InvokeCommand.ExpandString(op://$ENV:VAULT_NAME/$ENV:ITEM_NAME/$ENV:SECTION_NAME/Mobile)`
#
# vs
#
# `bash -ic 'echo op://$VAULT_NAME/$ITEM_NAME/$SECTION_NAME/Mobile'`
#
# This version of the mock (compared to the one in `test_service_account.py`),
# handwaves over how that command works, and what it returns, and instead just
# gives back a the `return_value` passed in that we're reasonably sure we're
# expecting back from `os.popen.read`.
@pytest.fixture()
def mock_popen_read(mocker):
    mock = mocker.Mock()
    mocker.patch("os.popen", return_value=mock)

    def _method(return_value=None):
        mock.read.return_value = return_value

    return _method

def test_no_env_vars_in_secret_reference():
    assert(
        secret_reference.expand_env_vars(
            "Darwin",
            "bash",
            "op://Plover/Personal/Phone/Mobile"
        ) == "op://Plover/Personal/Phone/Mobile"
    )

def test_expand_secret_reference_using_mac_or_linux(mocker, mock_popen_read):
    mock_popen_read(return_value="op://Plover/Personal/Phone/Mobile")
    spy = mocker.spy(os, "popen")

    assert(
        secret_reference.expand_env_vars(
            "Darwin",
            "bash",
            "op://$VAULT_NAME/$ITEM_NAME/$SECTION_NAME/Mobile"
        ) == "op://Plover/Personal/Phone/Mobile"
    )
    spy.assert_called_once_with(
        "bash -ic 'echo op://$VAULT_NAME/$ITEM_NAME/$SECTION_NAME/Mobile'"
    )

def test_expand_secret_reference_using_windows(mocker, mock_popen_read):
    mock_popen_read(return_value="op://Plover/Personal/Phone/Mobile")
    spy = mocker.spy(os, "popen")

    assert (
        secret_reference.expand_env_vars(
            "Windows",
            "bash",
            "op://$ENV:VAULT_NAME/$ENV:ITEM_NAME/$ENV:SECTION_NAME/Mobile"
        )
    ) == "op://Plover/Personal/Phone/Mobile"
    spy.assert_called_once_with(
        "echo $ExecutionContext.InvokeCommand.ExpandString("
        "op://$ENV:VAULT_NAME/$ENV:ITEM_NAME/$ENV:SECTION_NAME/Mobile)"
    )
