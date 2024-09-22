"""
Expander - a module for dealing with expansion of ENV vars in a secret
reference URI.
"""

import os
from typing import Callable


_ENV_VAR_SYNTAX: str = "$"

def expand_env_vars(
    shell_command: Callable[[str], str],
    secret_reference: str
) -> str:
    """
    Expands env vars in a secret reference. Returns immediately if no env vars
    contained in secret reference string.
    """
    if _ENV_VAR_SYNTAX not in secret_reference:
        return secret_reference

    command: str = shell_command(secret_reference)
    expanded: str = os.popen(command).read().strip()

    return expanded
