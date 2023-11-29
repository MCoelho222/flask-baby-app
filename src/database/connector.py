"""Create an instance of SQLAlchemy.

It will be used for database operations.
"""
from __future__ import annotations

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base SQLAlchemy Model.

    This module defines the base SQLAlchemy model class, 'Base'.
    Instances of 'Base' are used as the foundation for defining
    database models in the Light Data API.

    Usage:
    ------
    1. Inherit from 'Base' to define database models for the Light Data API.
    2. Use the 'db' instance for various database operations.

    Example:
    --------
    ```python
    class YourModel(Base):
        # Your model definition here
    """

    pass


db = SQLAlchemy(model_class=Base)
DBModel = db.Model
