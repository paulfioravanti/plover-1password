"""
Module to resolve a given 1Password secret reference URI to a secret contained
in a vault.
"""
from onepassword.client import Client

from ..__version__ import __version__
from . import error


_INTEGRATION_NAME = "Plover integration"

async def resolve(service_account_token: str, secret_reference: str) -> str:
    """
    Resolves a single secret from a secret reference URI.
    """
    if not secret_reference:
        raise ValueError("Secret Reference cannot be blank")

    try:
        client: Client = await _init_client(service_account_token)
        secret: str = await client.secrets.resolve(secret_reference)
    except Exception as exc: # pylint: disable=broad-except
        error.handle_ffi_error(exc)
        raise ValueError(str(exc)) from exc

    return secret

async def _init_client(service_account_token: str) -> Client:
    client: Client = await Client.authenticate(
        auth=service_account_token,
        integration_name=_INTEGRATION_NAME,
        integration_version=__version__
    )

    return client
