"""Functions for Occurrence entity operations."""
from __future__ import annotations

import logging

from sqlalchemy.exc import SQLAlchemyError

from data_api.database.connector import db
from data_api.helpers.exceptions import handle_exception_msg
from data_api.models.Occurrence import Occurrence

logger = logging.getLogger(__name__)


class OccurrenceController:
    """Define the methods for Occurrence entity operations."""

    @staticmethod
    def create(payload: dict[str, str]) -> dict[str, str]:
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
            db_occurrence = Occurrence(**payload)
            db.session.add(db_occurrence)
            db.session.commit()

            return db_occurrence.to_json()

        except SQLAlchemyError as e:
            msg = 'Failed to create Occurrence'
            logger.error('%s : %s', msg, e)
            db.session.rollback()
            return handle_exception_msg(e, msg)
