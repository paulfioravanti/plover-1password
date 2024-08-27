"""
# Secret

A package dealing with:
    - retrieving and resolving a secret from a 1Password vault
"""
from .resolver import (
    init_client,
    resolve
)

__all__ = [
    "init_client",
    "resolve"
]
