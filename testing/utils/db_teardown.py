"""Define functions fixtures teardown."""
from __future__ import annotations

from data_api.database.connector import db


def teardown_remove_all_from_db(entity: db.Model) -> None:
    """
    Remove all records from entity.

    Parameters
    ----------
        entity
            A SQLAlchemy model class.
    """
    els = db.session.query(entity).all()
    if els:
        for el in els:
            db.session.delete(el)
            db.session.commit()


def teardown_removeid_from_db(entity: db.Model, id: int) -> None:
    """
    Remove a record from entity based on its id.

    Parameters
    ----------
        entity
            A SQLAlchemy model class.
    """
    el = db.session.query(entity).filter(entity.id == id).first()
    if el:
        db.session.delete(el)
        db.session.commit()
