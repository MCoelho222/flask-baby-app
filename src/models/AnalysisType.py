"""
Module: analysis_schedule_model.py.

This module defines the SQLAlchemy model 'AnalysisSchedule' for
representing analysis schedules in the database.
"""
from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import humps

from data_api.database.connector import db
from data_api.helpers.exceptions import handle_exception_msg
from data_api.models.BaseModel import BaseModel

if TYPE_CHECKING:
    from data_api.helpers.exceptions import Error

logger = logging.getLogger(__name__)


class AnalysisType(BaseModel):
    """
    AnalysisType Class.

    Represents analysis types in the database.
    Inherits common functionalities from 'BaseModel'.

    Attributes
    ----------
        - id: Integer, primary key, auto-incremented identifier.
        - name: String, specifying the name of the analysis.
        - tag: String, a tag specifying the type of analysis.
        - description: String, a description of the analysis.
        - active: Boolean, indicates whether the analysis type is active.
        - icon: String, an HTML icon representing the anlaysis type.

    Methods
    -------
        to_json()
            Converts the Occurrence instance to a
            JSON representation.
    """

    __tablename__ = 'analysis_type'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    tag = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    metadata = db.Column(db.String, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    icon = db.Column(db.String, nullable=False)

    def to_json(self) -> str | Error:
        """
        Convert to json.

        Convert the Occurrence instance to a JSON representation.

        Returns
        -------
            A JSON of the Occurrence instance.
            If an error occurs during the conversion, the error is logged
            and dictionary with message and error is returned.
        """
        try:
            data = self.as_dict()
            data['id'] = str(self.id)

            data = json.dumps(data)

        except (TypeError, ValueError) as e:
            logger.exception(e)
            return handle_exception_msg(e, 'Failed to convert to JSON.')

        return humps.camelize(data)
