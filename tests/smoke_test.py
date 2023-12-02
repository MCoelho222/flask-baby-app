from __future__ import annotations

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import data_api
from data_api.__main__ import app
from data_api.auth.auth_decorators import token_required
from data_api.config import SQLALCHEMY_DATABASE_URI, config_by_name
from data_api.database.connector import db
from data_api.helpers.auth import get_public_key, has_required_roles
from data_api.helpers.exceptions import handle_exception_msg


def test_data_api_version():
    """Test import data_api correctly."""
    assert isinstance(data_api.__version__, str)


def test_app_instance():
    """Test if Flask instance is defined."""
    assert isinstance(app, Flask)


def test_sqlalchemy_database_uri():
    """Test if database url is correctly defined."""
    size = 4
    assert isinstance(SQLALCHEMY_DATABASE_URI, str)
    assert SQLALCHEMY_DATABASE_URI.startswith('postgresql+psycopg2://')
    assert len(SQLALCHEMY_DATABASE_URI.split(':')) == size


def test_token_decorator_defined():
    """Test if token decorator is defined."""
    assert callable(token_required)


def test_db_isinstance_sqlalchemy():
    """Test if a SQLAlchemy instance is mapped to db."""
    assert isinstance(db, SQLAlchemy)


def test_auth_helpers_defined():
    """Test if authentication helpers are defined."""
    assert callable(has_required_roles)
    assert callable(get_public_key)


def test_exception_helpers_defined():
    """Test if exception helpers are defined."""
    assert callable(handle_exception_msg)


def test_config_by_name():
    """Test if config object is correctly defined."""
    envs = ['production', 'development', 'testing']
    for env in envs:
        assert env in config_by_name
