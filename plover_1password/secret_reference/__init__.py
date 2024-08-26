"""
# Secret Reference

A package dealing with:
    - expanding local environment variables within a secret reference URI
"""
from .expander import expand_env_vars

__all__ = [
    "expand_env_vars"
]
