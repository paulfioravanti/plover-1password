"""
Token - Module concerning retrieving a token value for a 1Password Service
Account
"""
import os
from typing import Optional


_TOKEN_ENV_VAR_NAME: str = "OP_SERVICE_ACCOUNT_TOKEN"
_POWERSHELL_COMMAND: str = "echo $ENV:{0}"
_SHELL_COMMAND: str = "{0} -ic 'echo ${1}'"

def get_token(shell: Optional[str]=None) -> str:
    """
    Returns token from the local environment and errors if it is empty.
    """
    command: str
    if shell:
        command = _SHELL_COMMAND.format(shell, _TOKEN_ENV_VAR_NAME)
    else:
        command = _POWERSHELL_COMMAND.format(_TOKEN_ENV_VAR_NAME)

    token: Optional[str] = os.popen(command).read().strip()
    if not token:
        raise ValueError(f"No value found for ${_TOKEN_ENV_VAR_NAME}")

    return token
