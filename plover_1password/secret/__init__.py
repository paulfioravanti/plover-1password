"""
# Secret

A package dealing with:
    - retrieving and resolving a secret from a 1Password vault
"""
from .resolver import resolve

__all__ = [
    "resolve"
]
