"""
Expander - a module for dealing with expansion of ENV vars in a secret
reference URI.
"""

from typing import Callable

from .. import shell_command

_ENV_VAR_SYNTAX: str = "$"

def expand_env_vars(
    shell_command_resolver: Callable[[str], str],
    secret_reference: str
) -> str:
    """
    Expands env vars in a secret reference. Returns immediately if no env vars
    contained in secret reference string.
    """
    if _ENV_VAR_SYNTAX not in secret_reference:
        return secret_reference

    return shell_command.run(shell_command_resolver, secret_reference)
