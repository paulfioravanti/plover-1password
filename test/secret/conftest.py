import pytest


@pytest.fixture()
def mock_client(mocker):
    async_mock = mocker.AsyncMock()
    mocker.patch(
        "onepassword.client.Client.authenticate",
        return_value=async_mock
    )

    # REF: https://stackoverflow.com/a/8294654/567863
    def raise_(exc):
        raise exc

    # REF: https://stackoverflow.com/a/44701916/567863
    def _method(error_message="", return_value=None):
        if error_message:
            async_mock.secrets.resolve.side_effect = (
                lambda _return_value: raise_(Exception(error_message))
            )

        if return_value:
            async_mock.secrets.resolve.return_value = return_value

        return async_mock

    return _method
