"""Methods for CRUD operations in child classes."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from sqlalchemy.exc import SQLAlchemyError

from data_api.database.connector import DBModel, db
from data_api.helpers.errors import BussinesRulesError
from data_api.helpers.exceptions import handle_exception_msg

logger = logging.getLogger(__name__)

# Type-checking imports
if TYPE_CHECKING:
    from uuid import UUID

    from sqlalchemy.orm import Query


class BaseModel:
    """
    Provide common functionalities.

    BaseModel provides common functionality to be
    inherited by SQLAlchemy model classes.
    """

    __abstract__ = True

    @staticmethod
    def query(cls: DBModel) -> Query:
        """
        Construct and return an SQLAlchemy Query instance.

        Parameters
        ----------
            cls
                The SQLAlchemy model class.

        Returns
        -------
            An SQLAlchemy Query instance for
            the specified model class.
        """
        try:
            query = db.session.query(cls).select_from(cls)
            return query
        except SQLAlchemyError as e:
            msg = 'Query failed for %s.' % cls.__name__
            return handle_exception_msg(e, msg)

    @staticmethod
    def get_by_id_to_json(cls: DBModel, id: str | int | UUID) -> dict[str, str]:
        """
        Retrieve a dictionary representation of a database record based on its ID.

        Parameters
        ----------
            cls
                The SQLAlchemy model class.
            id
                The ID of the record to retrieve.

        Returns
        -------
            A dictionary representation of the record,
            or an empty dictionary if not found.
        """
        try:
            db_cls = cls.query(cls).filter(cls.id == id).first()
            if not db_cls:
                logger.info('No items found for id %s', id)
                return {}
            return cls.query_to_json(db_cls)

        except SQLAlchemyError as e:
            msg = 'Failed to get %s' % cls.__name__
            return handle_exception_msg(e, msg)

    @staticmethod
    def get_group_to_json(cls: DBModel, filter_obj: dict[str, Any]) -> list[dict[str, str]] | dict[str, str]:
        """
        Retrieve a list of entity items.

        Retrieve a list of dictionary representations of database
        records based on filtering criteria.

        Parameters
        ----------
            cls
                The SQLAlchemy model class.
            filter_obj
                A dictionary containing filtering criteria as
                key-value pairs.

        Returns
        -------
            A list of dictionary representations of matching
            records or a dictionary with error message.
        """
        group = []
        try:
            data = cls.query(cls)
            for key, value in filter_obj.items():
                if hasattr(cls, key):
                    data = data.filter(getattr(cls, key) == value)
                # value = filter_obj[key]
            data = data.all()
            if data:
                for row in data:
                    group.append(cls.query_to_json(row))
            if len(group) == 0:
                logger.info('No items found for specified filters: %s', filter_obj)
            return group

        except (TypeError, AttributeError, SQLAlchemyError) as e:
            msg = 'Failed to get %s.' % cls.__name__
            return handle_exception_msg(e, msg)

    @staticmethod
    def get_all_to_json(cls: DBModel) -> list[dict[str, str]] | dict[str, str]:
        """
        Retrieve all records from model.

        Retrieve all records of the specified SQLAlchemy model
        class and convert them to a list of dictionaries.

        Parameters
        ----------
            cls
                The SQLAlchemy model class.

        Returns
        -------
            - A list of dictionaries representing the records
            of the specified model class if records are found.
            - An empty list if no records are found.
            - A dictionary containing an error message if an
            exception occurs during the retrieval process.
        """
        try:
            data = []
            db_cls = cls.query(cls).all()
            if db_cls:
                for row in db_cls:
                    data.append(cls.query_to_json(row))
            if len(data) == 0:
                logger.info('No items found.')
            return data

        except SQLAlchemyError as e:
            msg = 'Failed to get %s.' % cls.__name__
            return handle_exception_msg(e, msg)

    @staticmethod
    def update(cls: DBModel, id: str | int | UUID, payload: dict[str, str]) -> list[dict[str, str]] | dict[str, str]:
        """
        Update a record of the model.

        Update a record of the specified SQLAlchemy model class with
        the provided payload.

        Parameters
        ----------
            cls
                The SQLAlchemy model class.
            id
                The identifier of the record to be updated.
            payload
                A dictionary containing the attributes and their
                updated values.

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
            db_cls = cls.query(cls).filter(cls.id == id).first()
            if not db_cls:
                logger.info('Items not found for specified id: %s', id)
                msg = 'Failed to update %s.' % cls.__name__
                return handle_exception_msg(BussinesRulesError(msg), 'id not found.')
            for key, value in payload.items():
                setattr(db_cls, key, value)
            db.session.commit()

            return db_cls.to_json()

        except SQLAlchemyError as e:
            db.session.rollback()
            msg = 'Failed to update %s.' % cls.__name__
            return handle_exception_msg(e, msg)

    @staticmethod
    def delete(cls: DBModel, id: str | int | UUID) -> list[dict[str, str]] | dict[str, str]:
        """
        Delete a record of the model.

        Delete a record of the specified SQLAlchemy model class by
        its identifier.

        Parameters
        ----------
            cls
                The SQLAlchemy model class.
            id
                The identifier of the record to be deleted.

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
            db_cls = cls.query(cls).filter(cls.id == id).first()

            if not db_cls:
                msg = 'Failed to update %s.' % cls.__name__
                return handle_exception_msg(BussinesRulesError(msg), 'id not found.')
            # if db_cls:
            db.session.delete(db_cls)
            # db_cls.is_deleted = True
            db.session.commit()

            return db_cls.to_json()

        except SQLAlchemyError as e:
            msg = 'Failed to delete %s.' % cls.__name__
            return handle_exception_msg(e, msg)
