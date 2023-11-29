"""Basic methods for child classes."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, Iterable, Iterator, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from data_api.helpers.exceptions import handle_exception_msg

# Type-checking imports
if TYPE_CHECKING:
    T = TypeVar('T')
    from uuid import UUID

    from sqlalchemy import Column, Table
    from sqlalchemy.orm import Session
    from typing_extensions import Self

    from data_api.helpers.exceptions import Error

log = logging.getLogger(__name__)


class BaseMixInModel:
    """
    Provide common functionalities.

    BaseMixInModel provides common functionality to be
    inherited by SQLAlchemy model classes.
    """

    __table__: Table
    id: Column
    name: Column

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """
        Yield pairs of column names and values.

        Iterate over the columns of the SQLAlchemy model
        and yield pairs of column names and values.

        Yields
        ------
            Pairs of column names and values for each
            column in the model.
        """
        for x in self.__class__.__table__.columns:
            yield x.name, self.__getattribute__(x.name)

    def __str__(self) -> str:
        """
        Generate a human-readable string.

        Generate a human-readable string representation of
        the SQLAlchemy model instance.

        Returns
        -------
            A formatted string representing the model
            instance, excluding the 'id' field.
        """
        fields = {k: getattr(self, k) for k in self.__class__.__table__.columns.keys() if k != 'id'}
        str_fields = ', '.join([f'{k}={v}' for k, v in fields.items()])
        return f'<{self.__class__.__name__} {self.id} ({str_fields})>'

    def __repr__(self) -> str:
        """
        Generate a string representation.

        Generate a string representation of the SQLAlchemy
        model instance suitable for debugging.

        Returns
        -------
            A string representation of the model instance,
            delegated to the __str__ method.
        """
        return str(self)

    @classmethod
    def get_by_id(cls, session: Session, obj_id: str | int | UUID) -> Self | Error | None:
        """
        Retrieve a Model instance by id from the database.

        Parameters
        ----------
            session
                SQLAlchemy session for the database connection.
            obj_id
                id to search for in the database.

        Returns
        -------
            - If the session is not an instance of
            sqlalchemy.orm.Session, returns a dictionary
            containing an error message.
            - If the obj_id is not str | int | UUID, returns a
            dictionary containing an error message.
            - If an instance of Model is found, returns
            the instance.
            - If no Model instance is found with the given
            name, returns None
            - If an SQLAlchemy error occurs during the query,
            raises an exception with an error message.
        """
        try:
            data = session.query(cls).filter(cls.id == obj_id).first()
            if not data:
                log.debug('No %s found with id: %s', cls.__name__, obj_id)
                # raise Exception(cls.__name__, 'ID')
            return data
        except SQLAlchemyError as e:
            log.exception(e)
            msg = f'Error querying {cls.__name__} by id: {obj_id}'
            return handle_exception_msg(e, msg)

    @classmethod
    def get_by_name(cls, session: Session, name: str) -> Self | Error | None:
        """
        Retrieve a Model instance by name from the database.

        Parameters
        ----------
            session
                SQLAlchemy session for the database connection.
            name
                Name to search for in the database.

        Returns
        -------
            - If the session is not an instance of
            sqlalchemy.orm.Session, returns a dictionary
            containing an error message.
            - If the name is not a string, returns a
            dictionary containing an error message.
            - If an instance of Model is found, returns
            the instance.
            - If no Model instance is found with the given
            name, returns None.
            - If an SQLAlchemy error occurs during the query,
            raises an exception with an error message.
        """
        try:
            data = session.query(cls).filter(cls.name == name).first()
            if not data:
                log.debug('No %s found with name: %s', cls.__name__, name)
            return data
        except SQLAlchemyError as e:
            log.exception(e)
            msg = f'Error querying {cls.__name__} by name: {name}'
            return handle_exception_msg(e, msg)

    @classmethod
    def get_all(cls, session: Session) -> list[Self] | Error:
        """
        Retrieve all records of the specified SQLAlchemy model class.

        Parameters
        ----------
            cls
                The SQLAlchemy model class.
            session : Session
                SQLAlchemy session for the database connection.

        Returns
        -------
            - A list of instances of the specified model class
            if records are found.
            - An empty list if no records are found.
            - A dictionary containing an error message
            if the session is not an instance of sqlalchemy.orm.Session.
        """
        try:
            data = session.query(cls).all()
            if len(data) == 0:
                log.debug('No %s found', cls.__name__)
            return data
        except SQLAlchemyError as e:
            log.exception(e)
            msg = f'Error querying {cls.__name__}'
            return handle_exception_msg(e, msg)

    @staticmethod
    def json_type(x: datetime | T) -> float | T:
        """
        Convert datetime objects to timestamps and leave other types unchanged.

        Parameters
        ----------
            x
                The input value to be converted, only if type is datetime.

        Returns
        -------
            Timestamp or x.
        """
        if isinstance(x, datetime):
            return x.timestamp()
        return x

    def as_dict(self, exclude: Iterable[str] = ()) -> dict[str, Any]:
        """
        Generate a dictionary representation of the class instance.

        Parameters
        ----------
            exclude
                Keys to exclude from the resulting dictionary.

        Returns
        -------
            The dictionary representation of the class instance.
        """
        try:
            as_dict = {k: self.json_type(getattr(self, k)) for k in self.__dict__ if k not in exclude}
            return as_dict
        except TypeError as e:
            msg = 'Failed to get dict representation of the instance.'
            return handle_exception_msg(e, msg)
