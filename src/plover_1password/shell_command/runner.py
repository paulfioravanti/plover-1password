"""
Runner - a module for running shell commands.
"""

import subprocess
from typing import Callable


def run(shell_command_resolver: Callable[[str], str], target: str) -> str:
    """
    Runs a provided shell command against target in a subprocess.
    """
    command: str = shell_command_resolver(target)
    result: str = subprocess.run(
        command,
        capture_output=True,
        check=False,
        encoding="utf-8",
        shell=True
    ).stdout.strip()

    return result
