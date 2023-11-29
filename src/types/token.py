"""Types for authentication tokens."""
from __future__ import annotations

from typing import NamedTuple


class KeycloakTokenType(NamedTuple):
    """
    KeycloakTokenType Class.

    A class representing the structure of a Keycloak token
    with typed attributes.
    """

    exp: int
    iat: int
    auth_time: int
    jti: str
    iss: str
    aud: str
    sub: str
    typ: str
    azp: str
    nonce: str
    session_state: str
    acr: str
    allowed_origins: list[str]
    realm_access: dict[str, list[str]]
    resource_access: dict[str, dict[str, list[str]]]
    scope: str
    sid: str
    email_verified: bool
    name: str
    preferred_username: str
    given_name: str
    family_name: str
    email: str
