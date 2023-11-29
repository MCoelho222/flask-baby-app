"""
Transmission Line Service API Module.

This module configures and provides the Transmission Line
Service API using Flask and Flask-RESTx. It defines a Flask
Blueprint with a RESTful API, including an 'occurrence' namespace.

Usage
-----
    1. Import this module and call the `configure_blueprint`
    function to obtain a configured Blueprint.
    2. Register the Blueprint with your Flask application.

Example
-------
    ```python
    from flask import Flask
    from your_module import configure_blueprint

    app = Flask(__name__)
    app.register_blueprint(configure_blueprint())

    if __name__ == "__main__":
        app.run()
"""
from __future__ import annotations

from flask import Blueprint, current_app
from flask_restx import Api

import data_api
from data_api.view.occurrence import api as occurrence_namespace


def configure_blueprint() -> None:
    """
    configure_blueprint Function.

    A function for configuring a Flask Blueprint and associating
    it with a Flask-RESTx API.

    Functionality
    -------------
        1. Creates a Flask Blueprint named 'api' with a specified
        URL prefix.
        2. Initializes a Flask-RESTx API associated with the
        blueprint.
        3. Sets the title, version, description, and security for
        the API.
        4. Adds namespaces to the API, specifying their paths.
        5. Registers the configured blueprint with the current
        Flask application.

    Usage
    -----
        This function is called during the setup of the Flask
        application to configure and associate a blueprint with
        a Flask-RESTx API. It defines the structure and details
        of the API, including its title, version, description,
        and security settings.
    """
    blueprint = Blueprint('api', __name__, url_prefix='/')

    api = Api(
        blueprint,
        title='Transmission Line Service API',
        version=data_api.__version__,
        description='Powered by Pix Force',
        security='apikey',
    )
    api.add_namespace(occurrence_namespace, path='/occurrence')

    current_app.register_blueprint(blueprint)
