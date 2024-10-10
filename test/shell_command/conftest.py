import pytest


@pytest.fixture()
def bash_command():
    def _method(shell):
        return lambda env_var: [f"{shell}", "-ic", f"echo {env_var}"]

    return _method
