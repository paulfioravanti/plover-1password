#!/usr/bin/env python3

from setuptools import setup

setup(
    extras_require = {
        "test": ["onepassword @ git+ssh://git@github.com/1Password/onepassword-sdk-python.git@v0.1.1"]
    }
)
