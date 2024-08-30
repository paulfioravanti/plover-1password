import os
import pytest

from plover_1password import shell_command

@pytest.fixture()
def bash_command():
    def _method(shell):
        return lambda env_var: f"{shell} -ic 'echo {env_var}'"

    return _method

def test_resolve_shell_command_for_windows(powershell_command):
    # REF: https://stackoverflow.com/a/20059029/567863
    assert (
        shell_command.resolve("Windows").__code__.co_code
        == powershell_command.__code__.co_code
    )

def test_resolve_shell_command_for_mac_or_linux(bash_command, monkeypatch):
    monkeypatch.setattr(os, "getenv", lambda _shell, _default_shell: "bash")

    # REF: https://stackoverflow.com/a/20059029/567863
    assert (
        shell_command.resolve("Darwin").__code__.co_code
        == bash_command("bash").__code__.co_code
    )
