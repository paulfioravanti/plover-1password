"""
Module to initialise a 1Password client
"""

from onepassword.client import Client

from ..__version__ import __version__


_INTEGRATION_NAME: str = "Plover 1Password plugin integration"

async def init_client(service_account_token: str) -> Client:
    """
    Initialises a 1Password client to retrieve secrets.
    """
    return (
        await Client.authenticate(
            auth=service_account_token,
            integration_name=_INTEGRATION_NAME,
            integration_version=__version__
        )
    )
