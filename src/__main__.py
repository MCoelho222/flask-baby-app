"""
Flask Baby App API Module.

This module contains the main components to run the API
using Flask. It includes functions to create the Flask application
(`create_app`), handle database sessions after each request
(`session_clear`), and serve as the main entry point for running
the API (`main`).

Usage:
-----
    - Run `flsk-baby-app` to start the Flask Baby App API.
"""
from __future__ import annotations

import logging

from flask import Flask
from flask_cors import CORS
from psycopg2.errors import OperationalError
from sqlalchemy.exc import SQLAlchemyError
from waitress import serve

import flask_baby_app
from flask_baby_app.config import ENV, FLASK_PORT, config_by_name
from flask_baby_app.database.connector import db
from flask_baby_app.helpers import log
from flask_baby_app.view import configure_blueprint

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    Create Flask App.

    Initialize a Flask app, configure it based
    on the environment specified by the 'ENV' variable,
    set up Cross-Origin Resource Sharing (CORS), and
    configure logging using the 'log' module.

    Returns
    -------
        An instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_by_name[ENV])

    CORS(app)
    CORS(app, resources={r'/*': {'origins': '*'}})

    log.setup(app)

    return app


app: Flask = create_app()


@app.teardown_request  # type: ignore[type-var] # NOTE: typing issue to be fixed in the future
def session_clear(exception: Exception) -> None:
    """
    Clear the database session after each request.

    Parameters
    ----------
        exception
            The exception that occurred during the
            request, if any.
    Usage
    -----
        Automatically called by Flask after each
        request, in case of an exception, roll back
        any uncommitted changes.
    """
    db.session.remove()
    if exception and db.session.is_active:
        db.session.rollback()


def main() -> None:
    """
    Entry point for running the Flask Baby App API.

    Initialize the database, configure the application,
    and start Flask development server or production server
    using the 'serve' function from the waitress
    module.

    Usage
    -----
        Run this script to start the Flask Baby App API.
    """
    logger.info('Flask Baby App Api, version %s is running on port %s', flask_baby_app.__version__, FLASK_PORT)

    try:
        db.init_app(app)
        with app.app_context():
            db.create_all()
    except SQLAlchemyError as e:
        logger.exception(e)
    except OperationalError as e:
        logger.exception(e)

    with app.app_context():
        configure_blueprint()

    if ENV == 'development':
        app.run(debug=config_by_name['development'].DEBUG, host='127.0.0.1', port=FLASK_PORT, use_reloader=True)
    # elif ENV == 'production':
    # app.run(ssl_context=('cert.pem', 'key.pem'))
    else:
        serve(app, host='0.0.0.0', port=FLASK_PORT)  # NOTE: is it really 0.0.0.0 in production? # noqa: S104


if __name__ == '__main__':
    raise SystemExit(main())  # type: ignore
