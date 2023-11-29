"""
Occurrence endpoint Module.

A module containing the implementation of the OccurrenceView class,
which represents the API endpoints for Occurrence-related operations
using Flask-RESTx. It includes methods for handling GET, POST, and
PUT requests related to Occurrence records, with authentication and
access control mechanisms.

Functionality
-------------
    - Defines the OccurrenceView class, a Flask-RESTx Resource, for
    handling Occurrence-related API endpoints.
    - Implements GET, POST, and PUT methods for retrieving, creating,
    and updating Occurrence records.
    - Utilizes decorators for authentication and role-based access
    control.
    - Parses and validates request parameters using Flask-RESTx.
"""
from __future__ import annotations

import logging

import humps
from flask_restx import Resource

from data_api.auth.auth_decorators import token_required
from data_api.controllers.OccurrenceController import OccurrenceController
from data_api.helpers.exceptions import Error
from data_api.models.Occurrence import Occurrence
from data_api.schemas.OccurrenceDto import OccurrenceDto

logger = logging.getLogger(__name__)

api = OccurrenceDto.api
parser = OccurrenceDto.parser
occurrence_create = OccurrenceDto.occurrence_model_create
occurrence_update = OccurrenceDto.occurrence_model_update


@api.route('/')
@api.route('/<string:id>')
class OccurrenceView(Resource):
    """
    OccurrenceView Resource.

    This resource provides endpoints for retrieving, creating, and editing Occurrences.

    Attributes
    ----------
        api
            The Flask-RESTx Api instance.

    Methods
    -------
        get(id=None)
            Get Occurrence.

        post()
            Create Occurrence.

        put(id)
            Edit Occurrence.
    """

    @api.doc('Occurrence [GET]', params={'type_tag': 'Tag of occurrence type'})
    @api.expect(parser)
    @token_required(required_roles=['user_role'])
    def get(self, id: str | None = None) -> tuple[dict[str, str], int]:
        """
        Get Occurrence.

        Parameters
        ----------
            id
                The ID of the Occurrence to retrieve.
            type_tag
                A string that represents the type of occurrence.

        Returns
        -------
            A tuple containing a dictionary with Occurrence data
            and an HTTP status code. In case of an error, the tuple
            includes an error message and an HTTP status code of 403.
        """
        logger.info('%s ...Get Occurrence...', __name__)
        args = parser.parse_args()
        type_tag = args.get('type_tag', None)
        if id:
            data = Occurrence.get_by_id_to_json(Occurrence, id)
        elif type_tag:
            data = Occurrence.get_group_to_json(Occurrence, {'type_tag': type_tag})
        else:
            data = Occurrence.get_all_to_json()

        if isinstance(data, Error):
            return data.to_dict(), 403

        return data

    @api.doc('Occurrence [POST]')
    @api.expect(occurrence_create, validate=True)
    @token_required(required_roles=['user_role'])
    def post(self) -> tuple[dict[str, str], int]:
        """
        Create Occurrence.

        Returns
        -------
            A tuple containing a dictionary with the newly
            created Occurrence data and an HTTP status code.
            In case of an error during creation, the tuple
            includes an error message and an HTTP status code
            of 403.
        """
        logger.info('%s ... Create Occurrence ...', __name__)

        payload = humps.decamelize(api.payload)
        controller = OccurrenceController()
        data = controller.create(payload)

        if isinstance(data, Error):
            return data.to_dict(), 403

        return data

    @api.doc('Occurrence [PUT]')
    @api.expect(occurrence_update, validate=True)
    @token_required(required_roles=['user_role'])
    def put(self, id: str) -> tuple[dict[str, str], int]:
        """
        Edit Occurrence.

        Parameters
        ----------
            id
                The ID of the Occurrence to edit.

        Returns
        -------
            tuple
                A tuple containing a dictionary with the updated
                Occurrence data and an HTTP status code. In case
                of an error during the update, the tuple includes
                an error message and an HTTP status code of 403.
        """
        logger.info('%s ...Edit Occurrence...', __name__)

        payload = humps.decamelize(api.payload)
        data = Occurrence.update(Occurrence, id, payload)

        if isinstance(data, Error):
            return data.to_dict(), 403

        return data
