from __future__ import annotations

import logging

import pytest
from keycloak.keycloak_openid import KeycloakOpenID

from flask_baby_app.__main__ import create_app
from flask_baby_app.database.connector import db
from flask_baby_app.view import configure_blueprint
from testing.helpers.keycloak import KeycloakData as kc

logger = logging.getLogger(__name__)


@pytest.fixture(scope='session')
def kc_client():
    keycloak_openid = KeycloakOpenID(
        server_url=kc.SERVER_URL,
        clientid=kc.BACKEND_CLIENTid,
        realm_name=kc.REALM,
        client_secret_key=kc.CLIENT_SECRET,
        verify=False,
    )

    return keycloak_openid


@pytest.fixture(scope='session')
def user_role_token(kc_client):
    token = kc_client.token(
        username=kc.LIGHT_USER,
        password=kc.LIGHT_USER_PASSWORD,
    )

    yield token

    kc_client.logout(token['refresh_token'])


@pytest.fixture(scope='session')
def no_user_role_token(kc_client):
    token = kc_client.token(
        username=kc.LIGHT_FORBIDDEN_USER,
        password=kc.LIGHT_FORBIDDEN_USER_PASSWORD,
    )

    yield token

    kc_client.logout(token['refresh_token'])


@pytest.fixture(scope='session')
def user_role_headers(user_role_token):
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype, 'Authorization': f'Bearer {user_role_token["access_token"]}'}

    return headers


@pytest.fixture(scope='session')
def no_user_role_headers(no_user_role_token):
    mimetype = 'application/json'
    headers = {'Content-Type': mimetype, 'Accept': mimetype, 'Authorization': f'Bearer {no_user_role_token["access_token"]}'}

    return headers


@pytest.fixture(scope='session')
def client():
    """Configures the app for testing
    Sets app config variable ``TESTING`` to ``True``
    :return: App for testing
    """

    flask_app = create_app()

    flask_app.config['TESTING'] = True
    db.init_app(flask_app)
    logger.info('Testing')

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            configure_blueprint()
            yield testing_client
