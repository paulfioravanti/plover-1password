import pytest

from plover_1password import secret


@pytest.fixture()
def mock_client(mocker):
    async_mock = mocker.AsyncMock()
    mocker.patch(
        "onepassword.client.Client.authenticate",
        return_value=async_mock
    )
    return async_mock

@pytest.fixture()
def patch_client_authenticate_error(monkeypatch):
    # REF: https://stackoverflow.com/questions/8294618/define-a-lambda-expression-that-raises-an-exception
    def raise_(exc):
        raise exc

    def _method(message=""):
        monkeypatch.setattr(
            "onepassword.client.Client.authenticate",
            lambda **kwargs: raise_(Exception(message))
        )

    return _method

async def test_blank_secret_reference():
    with pytest.raises(
        ValueError,
        match="Secret Reference cannot be blank"
    ):
        await secret.resolve("service_account_token", "")

async def test_service_account_token_invalid(patch_client_authenticate_error):
    patch_client_authenticate_error(
        message=(
            "invalid service account token, please make sure you provide a "
            "valid service account token as parameter: service account "
            "deserialization failed, please create another token"
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "Service Account Token is invalid. "
            "Create another token and restart Plover."
        )
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_service_account_token_invalid_format(
    patch_client_authenticate_error
):
    patch_client_authenticate_error(
        message=(
            "invalid user input: encountered the following errors: "
            "service account token had invalid format"
        )
    )

    with pytest.raises(
        ValueError,
        match=(
            "Service Account Token has invalid format. "
            "Fix token format or create a new one and restart Plover."
        )
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_secret_reference_invalid_format(mock_client):
    mock_client.secrets.resolve.side_effect = Exception(
        "error resolving secret reference: "
        "secret reference has invalid format - "
        "must be \"op://<vault>/<item>/[section/]field\""
    )

    with pytest.raises(
        ValueError,
        match=(
            "Secret Reference has invalid format. "
            "URI must be \"op://<vault>/<item>/\\[section/\\]field\""
        )
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_secret_reference_missing_prefix(mock_client):
    mock_client.secrets.resolve.side_effect = Exception(
        "error resolving secret reference: "
        "secret reference is not prefixed with \"op://\""
    )

    with pytest.raises(
        ValueError,
        match="Secret Reference needs to be prefixed with \"op://\""
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_secret_reference_vault_not_found(mock_client):
    mock_client.secrets.resolve.side_effect = Exception(
        "error resolving secret reference: "
        "no vault matched the secret reference query"
    )

    with pytest.raises(
        ValueError,
        match="Vault specified in Secret Reference not found."
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_secret_reference_item_not_found(mock_client):
    mock_client.secrets.resolve.side_effect = Exception(
        "error resolving secret reference: "
        "no item matched the secret reference query"
    )

    with pytest.raises(
        ValueError,
        match="Item specified in Secret Reference not found."
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_secret_reference_section_not_found(mock_client):
    mock_client.secrets.resolve.side_effect = Exception(
        "error resolving secret reference: "
        "no section matched the secret reference query"
    )

    with pytest.raises(
        ValueError,
        match="Section specified in Secret Reference not found."
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_secret_reference_field_not_found(mock_client):
    mock_client.secrets.resolve.side_effect = Exception(
        "error resolving secret reference: "
        "the specified field cannot be found within the item"
    )

    with pytest.raises(
        ValueError,
        match="Field specified Secret Reference not found."
    ):
        await secret.resolve("service_account_token", "secret_reference")

async def test_unexpected_exception(mock_client):
    mock_client.secrets.resolve.side_effect = Exception("Some exception")

    with pytest.raises(ValueError, match="Some exception"):
        await secret.resolve("service_account_token", "secret_reference")

async def test_successful_secret_retrieval(mock_client):
    mock_client.secrets.resolve.return_value = "secret"
    remote_secret = await secret.resolve(
        "service_account_token", "secret_reference"
    )
    assert remote_secret == "secret"
