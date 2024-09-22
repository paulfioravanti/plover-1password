"""
Plover entry point extension module for Plover 1Password

    - https://plover.readthedocs.io/en/latest/plugin-dev/extensions.html
    - https://plover.readthedocs.io/en/latest/plugin-dev/meta.html
"""

import asyncio
import platform
from typing import Callable

from plover.engine import StenoEngine
from plover.formatting import (
    _Action,
    _Context
)
from plover.registry import registry

from onepassword.client import Client

from . import (
    secret,
    secret_reference,
    service_account,
    shell_command
)


class OnePassword:
    """
    Extension class that also registers a meta plugin.
    The meta deals with retrieving secrets from 1Password
    """

    _client: Client
    _engine: StenoEngine
    _platform: str
    _shell_command: Callable[[str], str]

    def __init__(self, engine: StenoEngine) -> None:
        self._engine = engine

    def start(self) -> None:
        """
        Sets up the meta plugin and service account token.
        """
        self._platform = platform.system()
        self._shell_command = shell_command.resolve(self._platform)
        service_account_token = service_account.get_token(
            self._platform,
            self._shell_command
        )
        # The SDK client "sets up an authenticated session with the 1Password
        # servers and automatically refreshes it whenever it expires", so it
        # should hopefully be okay to locally cache a single client instance
        # here to handle all connections rather than create a new one on every
        # connection.
        # REF: https://developer.1password.com/docs/sdks/concepts/#state-management
        self._client = asyncio.run(
            secret.init_client(service_account_token)
        )
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
        op_secret_reference: str = secret_reference.expand_env_vars(
            self._shell_command,
            argument
        )
        secret_value: str = await secret.resolve(
            self._client,
            op_secret_reference
        )

        action: _Action = ctx.new_action()
        action.text = secret_value
        return action
