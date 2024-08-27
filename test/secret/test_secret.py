import pytest

from plover_1password import secret


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

async def test_initialising_a_client(mock_client):
    assert await secret.init_client("service_account_token") == mock_client()

async def test_blank_secret_reference(mock_client):
    with pytest.raises(
        ValueError,
        match="Secret Reference cannot be blank"
    ):
        await secret.resolve(mock_client, "")

async def test_service_account_token_invalid(mock_client):
    error_message = (
        "invalid service account token, please make sure you provide a "
        "valid service account token as parameter: service account "
        "deserialization failed, please create another token"
    )

    with pytest.raises(
        ValueError,
        match=(
            "Service Account Token is invalid. "
            "Create another token and restart Plover."
        )
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_service_account_token_invalid_format(mock_client):
    error_message = (
        "invalid user input: encountered the following errors: "
        "service account token had invalid format"
    )

    with pytest.raises(
        ValueError,
        match=(
            "Service Account Token has invalid format. "
            "Fix token format or create a new one and restart Plover."
        )
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_secret_reference_invalid_format(mock_client):
    error_message = (
        "error resolving secret reference: "
        "secret reference has invalid format - "
        "must be \"op://<vault>/<item>/[section/]field\""
    )

    with pytest.raises(
        ValueError,
        match=(
            "Secret Reference has invalid format. "
            "URI must be \"op://<vault>/<item>/\\[section/\\]field\". "
            "You provided secret_reference."
        )
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_secret_reference_missing_prefix(mock_client):
    error_message = (
        "error resolving secret reference: "
        "secret reference is not prefixed with \"op://\". "
        "You provided secret_reference."
    )

    with pytest.raises(
        ValueError,
        match="Secret Reference needs to be prefixed with \"op://\""
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_secret_reference_vault_not_found(mock_client):
    error_message = (
        "error resolving secret reference: "
        "no vault matched the secret reference query"
    )

    with pytest.raises(
        ValueError,
        match="Vault specified not found in Secret Reference secret_reference."
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_secret_reference_item_not_found(mock_client):
    error_message = (
        "error resolving secret reference: "
        "no item matched the secret reference query"
    )

    with pytest.raises(
        ValueError,
        match="Item specified not found in Secret Reference secret_reference."
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_secret_reference_section_not_found(mock_client):
    error_message = (
        "error resolving secret reference: "
        "no section matched the secret reference query"
    )

    with pytest.raises(
        ValueError,
        match=(
            "Section specified not found in Secret Reference secret_reference."
        )
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_secret_reference_field_not_found(mock_client):
    error_message = (
        "error resolving secret reference: "
        "the specified field cannot be found within the item"
    )

    with pytest.raises(
        ValueError,
        match="Field specified not found in Secret Reference secret_reference."
    ):
        await secret.resolve(
            mock_client(error_message=error_message),
            "secret_reference"
        )

async def test_unexpected_exception(mock_client):
    with pytest.raises(ValueError, match="Some exception"):
        await secret.resolve(
            mock_client(error_message="Some exception"), "secret_reference"
        )

async def test_successful_secret_retrieval(mock_client):
    remote_secret = await secret.resolve(
        mock_client(return_value="secret"),
        "secret_reference"
    )
    assert remote_secret == "secret"
