"""
Module: occurrence_model.py.

This module defines the SQLAlchemy model 'Occurrence' for
representing occurrences in the database. The 'Occurrence'
model inherits from 'BaseModel' and 'BaseMixInModel',
providing common functionalities.
"""
from __future__ import annotations

import json
import logging
from datetime import timedelta
from typing import Any

import humps

from data_api.database.connector import db
from data_api.helpers.exceptions import handle_exception_msg
from data_api.models.BaseMixInModel import BaseMixInModel
from data_api.models.BaseModel import BaseModel

logger = logging.getLogger(__name__)


class Occurrence(BaseModel, BaseMixInModel):
    """
    Occurrence Class.

    Represents an occurrence in the database.
    Inherits common functionalities from 'BaseModel'
    and 'BaseMixInModel'.

    Attributes
    ----------
        - id: Integer, primary key, auto-incremented identifier for occurrences.
        - type_tag: String, a tag specifying the type of occurrence.
        - description: String, a description of the occurrence.
        - resume: String, a summarized description of the occurrence.
        - active: Boolean, indicates whether the occurrence is active.
        - register_at: DateTime, timestamp indicating when the occurrence was registered.
        - update_at: DateTime, timestamp indicating the last update time of the occurrence.

    Methods
    -------
        query_to_json(object)
            Converts a SQLAlchemy object to a JSON
            representation.
        to_json()
            Converts the Occurrence instance to a
            JSON representation, handling datetime
            formatting.
    """

    __tablename__ = 'occurrence'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type_tag = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    resume = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    register_at = db.Column(db.DateTime(), nullable=False)
    update_at = db.Column(db.DateTime(), nullable=False)

    @staticmethod
    def query_to_json(object: Any) -> dict[str, str]:
        """
        Convert a SQLAlchemy object to a JSON representation.

        Parameters
        ----------
            object
                The SQLAlchemy object to be converted.

        Returns
        -------
            A dictionary representing the JSON representation
            of the SQLAlchemy object.
        """
        data = object.to_json()
        return data

    def to_json(self) -> dict[str, str]:
        """
        Convert to json.

        Convert the Occurrence instance to a JSON representation,
        handling datetime formatting.

        Returns
        -------
            A dictionary representing the JSON representation of
            the Occurrence instance. If an error occurs during the
            conversion, the error is logged, and an empty
            dictionary is returned.
        """
        try:
            data = self.as_dict(exclude=['register_at', 'update_at'])
            data['id'] = str(self.id)

            register_at_local = self.register_at - timedelta(hours=3)
            data['register_at'] = register_at_local.strftime('%Y-%m-%dT%H:%M:%S')
            update_at_local = self.update_at - timedelta(hours=3)
            data['update_at'] = update_at_local.strftime('%Y-%m-%dT%H:%M:%S')
            data = json.dumps(data)

        except (TypeError, ValueError) as e:
            logger.exception(e)
            return handle_exception_msg(e, 'Failed to convert to JSON.')

        return humps.camelize(data)
