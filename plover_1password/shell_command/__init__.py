"""
# Shell Command

A package dealing with:
    - resolve the platform-appropriate command to fetch environment variables
"""

__all__ = [
    "resolve",
    "run"
]

from .resolver import resolve
from .runner import run
