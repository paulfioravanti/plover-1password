"""
Token - Module concerning retrieving a token value for a 1Password Service
Account
"""

from typing import Callable

from .. import shell_command

_TOKEN_ENV_VAR_NAME: str = "OP_SERVICE_ACCOUNT_TOKEN"
_POWERSHELL_TOKEN_ENV_VAR_NAME: str = f"$ENV:{_TOKEN_ENV_VAR_NAME}"
_SHELL_TOKEN_ENV_VAR_NAME: str = f"${_TOKEN_ENV_VAR_NAME}"

def get_token(
    platform: str,
    shell_command_resolver: Callable[[str], str]
) -> str:
    """
    Returns token from the local environment and errors if it is empty.
    """
    token_env_var_name: str
    if platform == "Windows":
        token_env_var_name = _POWERSHELL_TOKEN_ENV_VAR_NAME
    else:
        token_env_var_name = _SHELL_TOKEN_ENV_VAR_NAME

    token: str = shell_command.run(shell_command_resolver, token_env_var_name)

    if not token:
        raise ValueError(f"No value found for {token_env_var_name}")

    return token
