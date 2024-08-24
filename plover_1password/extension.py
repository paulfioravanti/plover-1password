"""
Plover entry point extension module for Plover 1Password

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/meta.html
"""
import asyncio
from typing import Optional

from plover.engine import StenoEngine
from plover.formatting import (
    _Action,
    _Context
)
from plover.registry import registry

from onepassword.client import Client

from . import service_account
from .__version__ import __version__

_INTEGRATION_NAME = "Plover integration"

class OnePassword:
    """
    Extension class that also registers a meta plugin.
    The meta deals with retrieving secrets from 1Password
    """
    _engine: StenoEngine
    _service_account_token: Optional[str]

    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine

    def start(self) -> None:
        """
        Sets up the meta plugin and service account token.
        """
        self._service_account_token = service_account.get_token()
        registry.register_plugin(
            "meta",
            "1PASSWORD",
            lambda ctx, argument : asyncio.run(
                self._one_password(ctx, argument)
            )
        )

    def stop(self) -> None:
        """
        Stops the plugin -- no custom action needed.
        """

    async def _one_password(self, ctx: _Context, argument: str) -> _Action:
        """
        Retrieves a secret from 1Password based on the secret reference passed
        in as an argument in the steno outline, and outputs it.
        """
        client: Client = await Client.authenticate(
            auth=self._service_account_token,
            integration_name=_INTEGRATION_NAME,
            integration_version=__version__
        )
        value: str = await client.secrets.resolve(argument)

        action: _Action = ctx.new_action()
        action.text = value
        return action
