"""Basic methods for child classes."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, Iterable, Iterator, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from data_api.database.connector import db
from data_api.helpers.errors import BussinesRulesError
from data_api.helpers.exceptions import handle_exception_msg

# Type-checking imports
if TYPE_CHECKING:
    T = TypeVar('T')
    from uuid import UUID

    from sqlalchemy import Column, Table
    from sqlalchemy.orm import Query
    from typing_extensions import Self

    from data_api.helpers.exceptions import Error

logger = logging.getLogger(__name__)

session = db.session


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
    def query(cls) -> Query:
        """
        Construct and return an SQLAlchemy Query instance.

        Returns
        -------
            An SQLAlchemy Query instance for
            the specified model class.
        """
        try:
            query = session.query(cls).select_from(cls)
            return query

        except SQLAlchemyError as e:
            msg = 'Query failed for %s.' % cls.__name__
            return handle_exception_msg(e, msg)

    @staticmethod
    def query_to_json(query_object: Any) -> str:
        """
        Convert a SQLAlchemy object to a JSON representation.

        Parameters
        ----------
            query_object
                The SQLAlchemy object to be converted.

        Returns
        -------
            A dictionary representing the JSON representation
            of the SQLAlchemy object.
        """
        data = query_object.to_json()
        return data

    @classmethod
    def create(cls, payload: dict[str, Any], *, to_json: bool = False) -> str | Self | Error:
        """
        Create item in Occurrence entity.

        Parameters
        ----------
            payload
                Dictionary with the required fields from
                Occurrence entity.

        Returns
        -------
            json
                A json of the created item.
        """
        try:
            data = cls(**payload)
            db.session.add(data)
            db.session.commit()
            if data and to_json:
                return cls.query_to_json(data)
            return data

        except SQLAlchemyError as e:
            msg = 'Failed to create Occurrence.'
            logger.exception(e)
            db.session.rollback()
            return handle_exception_msg(e, msg)

    @classmethod
    def get(
        cls, id: str | int | UUID | None = None, *, to_json: bool = False
    ) -> Self | list[Self] | str | list[str] | Error | None:
        """
        Retrieve a Model instance from the database.

        Parameters
        ----------
            id
                id to search for in the database.
            to_json
                keyword-only argument. if true, instance is converted to json.

        Returns
        -------
            - If id is passed, return the instance with the id, otherwise
            return a list of all instances.
            - If an instance or instances of Model are found, returns
            the instance(s) or a json representation of the instance(s).
            - If no Model instance is found with the given
            name, returns None
            - If an SQLAlchemy error occurs during the query,
            raises an exception with an error message.
        """
        try:
            if id:
                data = cls.query().filter(cls.id == id).first()
                if not data:
                    logger.debug('No %s found with id: %s', cls.__name__, id)
            else:
                data = cls.query().all()
                if len(data) == 0:
                    logger.debug('No items found in %s.', cls.__name__)
            if data and to_json:
                if isinstance(data, list):
                    return [item.to_json() for item in data]
                return cls.query_to_json(data)
            return data

        except SQLAlchemyError as e:
            logger.exception(e)
            msg = f'Error querying {cls.__name__}'
            return handle_exception_msg(e, msg)

    @classmethod
    def update(cls, id: str | int | UUID, payload: dict[str, str], *, to_json: bool = False) -> Self | str | dict[str, str]:
        """
        Update a record of the model.

        Update a record of the specified SQLAlchemy model class with
        the provided payload.

        Parameters
        ----------
            id
                The identifier of the record to be updated.
            payload
                A dictionary containing the attributes and their
                updated values.
            to_json
                keyword-only argument. if true, instance is converted to json.

        Returns
        -------
            - A dictionary representing the updated record
            if the update is successful.
            - A dictionary containing an error message if the
            identifier is not found.
            - A dictionary containing an error message if an
            exception occurs during the update process.
        """
        try:
            data = cls.query().filter(cls.id == id).first()
            if not data:
                logger.info('Items not found for specified id: %s', id)
                msg = 'Failed to update %s.' % cls.__name__
                e = BussinesRulesError(msg)
                return handle_exception_msg(e, 'id not found.')
            for key, value in payload.items():
                setattr(data, key, value)
            session.commit()
            if data and to_json:
                return cls.query_to_json(data)
            return data

        except SQLAlchemyError as e:
            session.rollback()
            msg = 'Failed to update %s.' % cls.__name__
            return handle_exception_msg(e, msg)

    @classmethod
    def delete(cls, id: str | int | UUID | None = None, *, to_json: bool = False) -> Self | str | bool | Error:
        """
        Delete a record of the model.

        Delete a record of the specified SQLAlchemy model class by
        its identifier.

        Parameters
        ----------
            id
                The identifier of the record to be deleted.
            to_json
                keyword-only argument. if true, instance is converted to json.

        Returns
        -------
            - A dictionary representing the deleted record if
            the deletion is successful.
            - A dictionary containing an error message if the
            identifier is not found.
            - A dictionary containing an error message if an
            exception occurs during the deletion process.
        """
        try:
            if id:
                data = cls.query().filter(cls.id == id).first()

                if not data:
                    msg = f'Failed to delete id {id} from {cls.__name__}.'
                    e = BussinesRulesError(msg)
                    return handle_exception_msg(e, 'id not found.')
                # if data:
                # data.is_deleted = True
                session.delete(data)
                session.commit()
                if to_json:
                    return cls.query_to_json(data)
                return data
            else:
                session.delete()
                session.commit()
                msg = 'All items deleted from %s.' % cls.__name__
                logger.info(msg)
                return True

        except SQLAlchemyError as e:
            msg = 'Failed to delete %s.' % cls.__name__
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
            msg = 'Failed to get dict representation.'
            return handle_exception_msg(e, msg)
