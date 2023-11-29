"""Function for database operations during the tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from data_api.database.connector import db

if TYPE_CHECKING:
    from data_api.controllers.OccurrenceController import OccurrenceController
    from data_api.types.payloads import OccurrencePayloadType

    types_controllers = OccurrenceController  # in the future: Model1 | Model2 | ...


def create_and_returnid(
    entity: types_controllers, fields: OccurrencePayloadType | None = None, how_many: int | None = None
) -> int | list[int]:
    """
    Create a entity record and return its id.

    Parameters
    ----------
        entity
            A SQLAlchemy model class that has the create() method.
        fields
            The dictionary with at least the required {key: value, ...}
            pairs of the model.
        how_many
            The number of records to be created.

    Returns
    -------
        The id of the record or a list of records's ids.
    """
    if how_many:
        ids = []
        count = 0
        while count < how_many:
            if fields:
                create = entity.create(**fields)
            else:
                create = entity.create()
            db.session.add(create)
            db.session.commit()
            ids.append(int(create.id))
            count += 1

        return ids
    else:
        if fields:
            create = entity.create(**fields)
        else:
            create = entity.create()
        db.session.add(create)
        db.session.commit()

        return int(create.id)


def create_and_return_entity(
    entity: types_controllers, fields: OccurrencePayloadType | None = None, how_many: int | None = None
) -> dict[str, str] | list[dict[str, str]]:
    """
    Create an entity record and return a json of the entity.

    Parameters
    ----------
        entity
            A SQLAlchemy model class that has the create() method.
        fields
            The dictionary with at least the required {key: value, ...}
            pairs of the model.
        how_many
            The number of records to be created.

    Returns
    -------
        A json of the record or a list of jsons.
    """
    if how_many:
        ids = []
        count = 0
        while count < how_many:
            if fields:
                entity_ = entity.create(**fields)
            else:
                entity_ = entity.create()
            db.session.add(entity_)
            db.session.commit()
            ids.append(entity_)
            count += 1

        return ids
    else:
        if fields:
            entity_ = entity.create(**fields)
        else:
            entity_ = entity.create()
        db.session.add(entity_)
        db.session.commit()

        return entity_


def queryids(entity: db.Model) -> list[int]:
    """
    Query items from a database entity.

    Parameters
    ----------
        entity
            A SQLAlchemy model class.
    """
    ids = []
    items = db.session.query(entity).all()
    for item in items:
        id = int(item.id)
        ids.append(id)

    return ids
