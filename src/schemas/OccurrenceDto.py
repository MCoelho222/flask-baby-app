"""
OccurrenceDto Module.

Defines a Flask-RESTx namespace and related models for
handling occurrence-related operations.

Usage
-----
    The module is designed to be used in a Flask-RESTx application
    to define and handle API endpoints related to occurrences.
"""
from __future__ import annotations

from flask_restx import Namespace, fields, reqparse

occurrence_model = {
    'type_tag': fields.String(required=True, description='Tag of the occurrence type'),
    'description': fields.String(required=False, description='Description of the occurrence'),
    'resume': fields.String(required=True, description='Resume of the occurrence'),
    'active': fields.Boolean(required=True, description='Status of the occurrence'),
    'register_at': fields.DateTime(required=True, description='Register of the occurrence'),
    'update_at': fields.DateTime(required=True, description='Update of the occurrence'),
}

occurrence_model_update = {
    'type_tag': fields.String(required=False, description='Tag of the occurrence type'),
    'description': fields.String(required=False, description='Description of the occurrence'),
    'resume': fields.String(required=False, description='Resume of the occurrence'),
    'active': fields.Boolean(required=False, description='Status of the occurrence'),
}


class OccurrenceDto:
    """
    OccurrenceDto Class.

    A class encapsulating the Flask-RESTx namespace, models,
    and request parser for occurrence-related operations.

    Usage
    -----
        The class is designed to be instantiated in a Flask-RESTx
        application to organize and manage the namespace, models,
        and request parser related to occurrences.

    Example
    -------
        ```python
        occurrence_dto = OccurrenceDto()
        api.add_namespace(occurrence_dto.api)
        ```
    """

    api = Namespace('occurrence', description='Occurrence related operations')
    occurrence_model_create = api.model('occurrence_model_create', occurrence_model)
    occurrence_model_update = api.model('occurrence_model_update', occurrence_model_update, strict=True)

    parser = reqparse.RequestParser()
    parser.add_argument('gap_cod', type=str, required=False, help='Identifier code of the Gap')
    parser.add_argument('type_tag', type=str, required=False, help='Tag of occurrence type')
    parser.add_argument('line_name', type=str, required=False, help='Name of the transmission line')
