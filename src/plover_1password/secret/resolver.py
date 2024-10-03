"""
Module to resolve a given 1Password secret reference URI to a secret contained
in a vault.
"""

from onepassword.client import Client

from . import error


async def resolve(client: Client, secret_reference: str) -> str:
    """
    Resolves a single secret from a secret reference URI.
    """
    if not secret_reference:
        raise ValueError("Secret Reference cannot be blank")

    try:
        secret: str = await client.secrets.resolve(secret_reference)
    except Exception as exc: # pylint: disable=broad-except
        error.handle_ffi_error(exc, secret_reference)
        raise ValueError(exc) from exc

    return secret
