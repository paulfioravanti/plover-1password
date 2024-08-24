"""
Token - Module concerning retrieving a token value for a 1Password Service
Account
"""

from typing import Optional
import os
import platform


_DEFAULT_SHELL = "bash"
_TOKEN_ENV_VAR_NAME = "OP_SERVICE_ACCOUNT_TOKEN"
_POWERSHELL_COMMAND = "echo $ENV:{0}"
_SHELL_COMMAND = "{0} -ic 'echo ${1}'"

def get_token() -> str:
    """
    Returns token from the local environment and errors if it is empty.
    """
    command: str
    if platform.system() == "Windows":
        command = _POWERSHELL_COMMAND.format(_TOKEN_ENV_VAR_NAME)
    else:
        shell: Optional[str] = os.getenv("SHELL", _DEFAULT_SHELL).split("/")[-1]
        command = _SHELL_COMMAND.format(shell, _TOKEN_ENV_VAR_NAME)

    token: Optional[str] = os.popen(command).read().strip()
    if not token:
        raise ValueError(f"No value found for ${_TOKEN_ENV_VAR_NAME}")

    return token
