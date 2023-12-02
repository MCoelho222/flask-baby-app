"""
Configurations for Flask Baby App Api.

1. Set the SQLALCHEMY_DATABASE_URI
2. Set the development and production classes
3. Create the config_by_name dictionary
"""
from __future__ import annotations

import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

if os.environ.get('FLASK_ENV') == 'production':
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=os.environ.get('DB_USER_PROD'),
        passwd=os.environ.get('DB_PASS_PROD'),
        host=os.environ.get('DB_HOST_PROD'),
        port=os.environ.get('DB_PORT_PROD'),
        db=os.environ.get('DB_NAME_PROD'),
    )

if os.environ.get('FLASK_ENV') == 'testing':
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=os.environ.get('DB_USER_TEST'),
        passwd=os.environ.get('DB_PASS_TEST'),
        host=os.environ.get('DB_HOST_TEST'),
        port=os.environ.get('DB_PORT_TEST'),
        db=os.environ.get('DB_NAME_TEST'),
    )
else:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=os.environ.get('DB_USER_DEV'),
        passwd=os.environ.get('DB_PASS_DEV'),
        host=os.environ.get('DB_HOST_DEV'),
        port=os.environ.get('DB_PORT_DEV'),
        db=os.environ.get('DB_NAME_DEV'),
    )


ENV = os.environ.get('FLASK_ENV')
FLASK_PORT = os.environ.get('FLASK_PORT')

KC_REALM = os.environ.get('KC_REALM')
KC_SERVER_URL = os.environ.get('KC_SERVER_URL')
KC_BACKEND_CLIENT_ID = os.environ.get('KC_BACKEND_CLIENT_ID')
KC_CLIENT_SECRET = os.environ.get('KC_BACKEND_CLIENT_SECRET')


class Config:
    """Set the environmental variables for the api."""

    DEBUG: bool = False
    SESSION_TYPE: str = 'filesystem'
    SESSION_PERMANENT: bool = True
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = True
    SQLALCHEMY_DATABASE_URI: str = SQLALCHEMY_DATABASE_URI
    TEMPLATES_AUTO_RELOAD: bool = True
    JWT_SECRET_KEY: str | None = os.environ.get('SECRET_KEY')

    PROPAGATE_EXCEPTIONS: bool = True


class DevelopmentConfig(Config):
    """Set environmental variables for development."""

    DEBUG = True

    FRONTEND_URL = os.environ.get('FRONTEND_URL_DEV')
    VISION_BACK_END_URL = os.environ.get('VISION_BACKEND_URL_DEV')


class ProductionConfig(Config):
    """Set environmental variables for production."""

    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    FRONTEND_URL = os.environ.get('FRONTEND_URL_PROD')
    VISION_BACKEND_URL = os.environ.get('VISION_BACKEND_URL_PROD')


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': DevelopmentConfig,
}
