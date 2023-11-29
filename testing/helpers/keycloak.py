"""
Keycloak Configuration Module.

This module defines a class, KeycloakData, representing configuration data
for Keycloak authentication. It includes attributes for various Keycloak
settings such as the realm, server URL, client ID, client secret, and user
credentials for testing purposes.
"""
from __future__ import annotations

import os


class KeycloakData:
    """
    A class representing configuration data for Keycloak authentication.

    These variables are used get a token from keycloak authentication
    service, and then use for testing purposes.
    """

    REALM = os.environ.get('KC_REALM')
    SERVER_URL = os.environ.get('KC_SERVER_URL')
    BACKEND_CLIENTid = os.environ.get('KC_BACKEND_CLIENTid')
    CLIENT_SECRET = os.environ.get('KC_BACKEND_CLIENT_SECRET')

    LIGHT_USER = os.environ.get('LIGHT_USER')
    LIGHT_USER_PASSWORD = os.environ.get('LIGHT_USER_PASSWORD')
    LIGHT_FORBIDDEN_USER = os.environ.get('LIGHT_FORBIDDEN_USER')
    LIGHT_FORBIDDEN_USER_PASSWORD = os.environ.get('LIGHT_FORBIDDEN_USER_PASSWORD')

    INVALID_TOKEN = os.environ.get('KC_INVALID_TOKEN')
