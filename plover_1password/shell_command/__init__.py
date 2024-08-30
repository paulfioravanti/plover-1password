"""
# Shell Command

A package dealing with:
    - resolve the platform-appropriate command to fetch environment variables
"""
from .resolver import resolve

__all__ = [
    "resolve"
]
