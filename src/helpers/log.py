"""Set Loggers for the app."""
from __future__ import annotations

import datetime as dt
import json
import logging
import pathlib as pl
import sys
import time
from logging.handlers import TimedRotatingFileHandler

import flask
from flask import Flask, Response, request

from flask_baby_app.config import ENV


def setup(app: Flask) -> None:
    """
    Set up logging configuration for a Flask application.

    - Set up a console handler for logging messages to the console with a specific log format.
    - Set up a file handler for logging messages to a rotating log file with a specific log format.
      The log file is rotated daily at midnight, and the
      logs are written in Coordinated Universal Time (UTC).
      If the Flask environment is 'testing', a separate log
      file is used for tests.
    - Configure the 'werkzeug' logger to log only errors.
    - Register a 'before_request' middleware that records the start time of each incoming request.
    - Registers an 'after_request' middleware that logs information about the request and response.

    Request/Response Logging
    ------------------------
        Log details such as method, path, status code,
        duration, IP address, host, query parameters, and
        request ID for each incoming request and outgoing
        response.

    Parameters
    ----------
        app
            The Flask application instance to which the
            logging configuration and middleware will be
            applied.

    Notes
    -----
        Ensure that this function is called during the
        application setup process to configure logging and
        enable request/response logging middleware.

    Example
    -------
        ```python
        from flask import Flask
        from your_module import setup

        app = Flask(__name__)
        setup(app)
        ```
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter('%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(message)s')

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    log_dir = pl.Path('logs').expanduser().resolve()
    log_dir.mkdir(parents=True, exist_ok=True)
    file_name = 'auditor.log'
    if ENV == 'testing':
        file_name = 'tests_auditor.log'
    file_handler = TimedRotatingFileHandler(log_dir / file_name, when='midnight', atTime=dt.time(hour=1), utc=True)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # register logger to app
    @app.before_request
    def start_timer() -> None:
        flask.g.start = time.time()

    @app.after_request
    def log_response_info(response: Response) -> Response:
        """
        Log details after processing a request.

        Parameters
        ----------
        response
            The Flask response object generated by the
            route handler.

        Returns
        -------
        Response
            The original Flask response object.

        Notes
        -----
            This function logs information such as method,
            path, status code, duration, IP address, host,
            query parameters, and request ID for each incoming
            request and outgoing response.
        """
        now = time.time()
        duration = round(now - flask.g.start, 2)

        requestid = request.headers.get('X-Request-ID')
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host.split(':', 1)[0]
        args = dict(request.args)

        parts = [
            f'method={request.method}',
            f'path={request.path}',
            f'status_code={response.status_code}',
            f'duration={duration}',
            f'ip={ip}',
            f'host={host}',
            f'params={args}',
            f'requestid={requestid}',
        ]

        line = ' '.join(parts)
        app.logger.info(line)

        return response


def jprint(parsed: dict[str, str]) -> None:
    """
    Pretty-print JSON data for debugging purposes.

    Parameters
    ----------
        parsed
            The data to be pretty-printed as JSON.

    Notes
    -----
        This function logs the pretty-printed JSON data at
        the DEBUG log level.
    """
    logging.getLogger(__name__).debug(json.dumps(parsed, indent=4, sort_keys=True))
