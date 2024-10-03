"""
# Secret

A package dealing with:
    - retrieving and resolving a secret from a 1Password vault
"""

__all__ = [
    "init_client",
    "resolve"
]

from .client import init_client
from .resolver import resolve
