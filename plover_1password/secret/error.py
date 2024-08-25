"""
Module to handle errors raised from 1Password's uniffi_core C shared libraries
but not handled in the Python SDK.
See: https://github.com/1Password/onepassword-sdk-python/tree/main/src/onepassword/lib
"""
_SERVICE_ACCOUNT_TOKEN_INVALID_ERROR = (
    "invalid service account token, please make sure you provide a valid "
    "service account token as parameter: service account deserialization "
    "failed, please create another token"
)
_SERVICE_ACCOUNT_TOKEN_INVALID_FORMAT_ERROR = (
    "invalid user input: encountered the following errors: "
    "service account token had invalid format"
)
_SECRET_REFERENCE_INVALID_FORMAT_ERROR = (
    "error resolving secret reference: "
    "secret reference has invalid format - "
    "must be \"op://<vault>/<item>/[section/]field\""
)
_SECRET_REFERENCE_MISSING_PREFIX_ERROR = (
    "error resolving secret reference: "
    "secret reference is not prefixed with \"op://\""
)
_SECRET_REFERENCE_VAULT_NOT_FOUND_ERROR = (
    "error resolving secret reference: "
    "no vault matched the secret reference query"
)
_SECRET_REFERENCE_ITEM_NOT_FOUND_ERROR = (
    "error resolving secret reference: "
    "no item matched the secret reference query"
)
_SECRET_REFERENCE_SECTION_NOT_FOUND_ERROR = (
    "error resolving secret reference: "
    "no section matched the secret reference query"
)
_SECRET_REFERENCE_FIELD_NOT_FOUND_ERROR = (
    "error resolving secret reference: "
    "the specified field cannot be found within the item"
)

def handle_ffi_error(exc: Exception) -> None:
    """
    Handles errors generated from 1Password's ffi libraries and re-raises them
    with more plugin-relevant messages.
    """
    error_message: str = str(exc)

    if _SERVICE_ACCOUNT_TOKEN_INVALID_ERROR in error_message:
        raise ValueError(
            "Service Account Token is invalid. "
            "Create another token and restart Plover."
        ) from exc

    if _SERVICE_ACCOUNT_TOKEN_INVALID_FORMAT_ERROR in error_message:
        raise ValueError(
            "Service Account Token has invalid format. "
            "Fix token format or create a new one and restart Plover."
        ) from exc

    if _SECRET_REFERENCE_INVALID_FORMAT_ERROR in error_message:
        raise ValueError(
            "Secret Reference has invalid format. "
            "URI must be \"op://<vault>/<item>/[section/]field\""
        ) from exc

    if _SECRET_REFERENCE_MISSING_PREFIX_ERROR in error_message:
        raise ValueError(
            "Secret Reference needs to be prefixed with \"op://\""
        ) from exc

    if _SECRET_REFERENCE_VAULT_NOT_FOUND_ERROR in error_message:
        raise ValueError(
            "Vault specified in Secret Reference not found."
        ) from exc

    if _SECRET_REFERENCE_ITEM_NOT_FOUND_ERROR in error_message:
        raise ValueError(
            "Item specified in Secret Reference not found."
        ) from exc

    if _SECRET_REFERENCE_SECTION_NOT_FOUND_ERROR in error_message:
        raise ValueError(
            "Section specified in Secret Reference not found."
        ) from exc

    if _SECRET_REFERENCE_FIELD_NOT_FOUND_ERROR in error_message:
        raise ValueError(
            "Field specified Secret Reference not found."
        ) from exc
