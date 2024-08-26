"""
Expander - a module for dealing with expansion of ENV vars in a secret
reference URI.
"""
import os
from typing import Optional


_ENV_VAR_SYNTAX = "$"
_POWERSHELL_COMMAND = "echo $ExecutionContext.InvokeCommand.ExpandString({0})"
_SHELL_COMMAND = "{0} -ic 'echo {1}'"

def expand_env_vars(
    system: str,
    shell: Optional[str],
    secret_reference: str
) -> str:
    """
    Expands env vars in a secret reference. Returns immediately if no env vars
    contained in secret reference string.
    """
    if not _ENV_VAR_SYNTAX in secret_reference:
        return secret_reference

    command: str
    if system == "Windows":
        command = _POWERSHELL_COMMAND.format(secret_reference)
    else:
        command = _SHELL_COMMAND.format(shell, secret_reference)

    expanded: str = os.popen(command).read().strip()

    return expanded
