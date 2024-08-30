"""
# Secret

A package dealing with:
    - retrieving and resolving a secret from a 1Password vault
"""
from .client import init_client
from .resolver import resolve

__all__ = [
    "init_client",
    "resolve"
]
