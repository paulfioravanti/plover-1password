#!/usr/bin/env python3

from setuptools import setup
import os

setup(
    # NOTE: Remove this and the vendored file once 1Password SDK is published to
    # PyPI.
    # REF: https://github.com/1Password/onepassword-sdk-python/issues/107
    install_requires = [
        f"onepassword @ file://{os.getcwd()}/vendor/onepassword-sdk-python-0.1.1.zip"
    ]
)
