"""
Token - Module concerning retrieving a token value for a 1Password Service
Account
"""

import os
from typing import (
    Callable,
    Optional
)

_TOKEN_ENV_VAR_NAME: str = "OP_SERVICE_ACCOUNT_TOKEN"
_POWERSHELL_TOKEN_ENV_VAR_NAME: str = f"$ENV:{_TOKEN_ENV_VAR_NAME}"
_SHELL_TOKEN_ENV_VAR_NAME: str = f"${_TOKEN_ENV_VAR_NAME}"

def get_token(platform: str, shell_command: Callable[[str], str]) -> str:
    """
    Returns token from the local environment and errors if it is empty.
    """
    token_env_var_name: str
    if platform == "Windows":
        token_env_var_name = _POWERSHELL_TOKEN_ENV_VAR_NAME
    else:
        token_env_var_name = _SHELL_TOKEN_ENV_VAR_NAME

    command: str = shell_command(token_env_var_name)
    token: Optional[str] = os.popen(command).read().strip()

    if not token:
        raise ValueError(f"No value found for {token_env_var_name}")

    return token
