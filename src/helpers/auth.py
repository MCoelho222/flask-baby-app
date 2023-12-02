"""Functions for authentication decorator."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Iterable

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate

from flask_baby_app.helpers.errors import BussinesRulesError

# Type-checking imports
if TYPE_CHECKING:
    from types.token import KeycloakTokenType

    from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
    from keycloak.keycloak_openid import KeycloakOpenID

logger = logging.getLogger(__name__)


def has_required_roles(token_decoded: KeycloakTokenType, required_roles: Iterable[str]) -> bool:
    """
    Verify if a user or client has the required roles for the endpoint.

    Parameters
    ----------
        token_decoded
            The parsed token from keycloak.
        required_roles
            A list or tuple of strings representing the roles.

    Returns
    -------
        True, if the user has the required roles, {'error': str, 'message': str} otherwise.
    """
    required_set = set(required_roles)
    realm_access = token_decoded.get('realm_access', {})
    if isinstance(realm_access, dict):
        roles: Iterable[str] = set(realm_access.get('roles', []))
        has_required_roles = required_set.issubset(roles) if roles else False
        missing_roles = list(required_set.difference(roles)) if roles else []
        if has_required_roles:
            return True
        else:
            sep = ', '
            missing_roles_str = sep.join(missing_roles) if len(missing_roles) > 1 else missing_roles[0]
            logger.exception(BussinesRulesError(missing_roles_str))
            return False
    return False


def get_public_key(keycloak_client: KeycloakOpenID) -> RSAPublicKey:
    """
    Get public key from keycloak realm.

    Parameters
    ----------
        keycloak_client

    Returns
    -------
        The public key.
    """
    certs = keycloak_client.certs()
    sig_cert = ''
    if certs:
        for cert in certs['keys']:
            if cert['use'] == 'sig':
                sig_cert = cert['x5c'][0]

    KC_CERTIFICATE = f"""
    -----BEGIN CERTIFICATE-----
    {sig_cert}
    -----END CERTIFICATE-----
    """
    cert_obj = load_pem_x509_certificate(KC_CERTIFICATE.encode(), default_backend())
    KC_PUBLIC_KEY = cert_obj.public_key()
    public_bytes = KC_PUBLIC_KEY.public_bytes(
        encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    decoded_key = serialization.load_pem_public_key(public_bytes, backend=default_backend())

    return decoded_key
