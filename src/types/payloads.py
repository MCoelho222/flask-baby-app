"""
Type classes for payloads.

This module has classes with attributes that specify
the type of each field in the SQLAlchemy model classes.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from datetime import datetime


class OccurrencePayloadType(NamedTuple):
    """Specify the type for each field in the Occurrence model."""

    type_tag: str
    description: str | None
    resume: str
    active: bool
    register_at: datetime
    update_at: datetime
