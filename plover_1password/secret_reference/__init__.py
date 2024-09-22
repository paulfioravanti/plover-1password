"""
# Secret Reference

A package dealing with:
    - expanding local environment variables within a secret reference URI
"""

__all__ = [
    "expand_env_vars"
]

from .expander import expand_env_vars
