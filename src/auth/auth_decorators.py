"""Decorators related to client and user authentication."""
from __future__ import annotations

import logging
from functools import wraps
from typing import Callable, Iterable, ParamSpec, TypeVar

from flask import request
from keycloak.exceptions import KeycloakError
from keycloak.keycloak_openid import KeycloakOpenID

from data_api.config import KC_BACKEND_CLIENT_ID, KC_CLIENT_SECRET, KC_REALM, KC_SERVER_URL
from data_api.helpers.auth import get_public_key, has_required_roles
from data_api.helpers.errors import BussinesRulesError
from data_api.helpers.exceptions import Error, handle_exception_msg

logger = logging.getLogger(__name__)

P = ParamSpec('P')
F = TypeVar('F')


def token_required(required_roles: Iterable[str]) -> Callable[[Callable[P, F]], Callable[P, F | tuple[Error, int]]]:
    """
    Require a valid token with specified roles.

    Parameters
    ----------
    required_roles
        Roles required to access the decorated route.

    Returns
    -------
        Decorated function.
    """

    def _token_required(f: Callable[P, F]) -> Callable[P, F | tuple[Error, int]]:
        """
        Wrap token_required decorator.

        Parameters
        ----------
            f
                Original function to be decorated.

        Returns
        -------
            Decorated function.
        """

        @wraps(f)
        def decorated_function(*args: P.args, **kwargs: P.kwargs) -> F | tuple[dict[str, str], int] | tuple[Error, int]:
            """
            Check if the request has a valid token with the required roles.

            Parameters
            ----------
                *args
                    Variable positional arguments.
                **kwargs
                    Variable keyword arguments.

            Returns
            -------
                - A tuple containing the result and status code if there is an error.
                - The original function if the token is valid and has the required roles.
            """
            authorization = request.headers.get('Authorization', None)
            token = None

            if authorization:
                token = authorization.split(' ')[1]

            keycloak_openid = KeycloakOpenID(
                server_url=KC_SERVER_URL,
                clientid=KC_BACKEND_CLIENT_ID,
                realm_name=KC_REALM,
                client_secret_key=KC_CLIENT_SECRET,
                verify=False,
            )
            decoded_key = get_public_key(keycloak_openid)

            try:
                is_valid_token = keycloak_openid.decode_token(
                    token,
                    key=decoded_key,
                    algorithms=['RS256'],
                    options={'verify_aud': False, 'verify_iat': False, 'verify_exp': True},
                )

                # if is_valid_token:
                has_permission = has_required_roles(is_valid_token, required_roles)
                if not has_permission:
                    msg = 'Missing one or more roles.'
                    raise BussinesRulesError(msg)

                return f(*args, **kwargs)

            except (KeycloakError, BussinesRulesError) as e:
                logger.exception(e)
                return handle_exception_msg(e, 'Authentication failed or user without permission.'), 403

        return decorated_function

    return _token_required
