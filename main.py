"""Main package."""

from celery import Celery
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_restx import Api
from flask_cors import CORS

from marshmallow import ValidationError as MarshmallowError

from api import api_blueprint
from api.middlewares.base_validator import (ValidationError,
                                            middleware_blueprint)
from api.models.database import db
from api.utilities.constants import EXCLUDED_KEYS
from config import AppConfig

TASK_LIST = ['api.tasks.email_sender']

api = Api(api_blueprint, security='Bearer Auth', doc='/documentation/')
celery_app = Celery(__name__, broker=AppConfig.REDIS_URL, include=TASK_LIST)


def initialize_errorhandlers(application):
    """Initializing error handlers."""
    application.register_blueprint(middleware_blueprint)
    application.register_blueprint(api_blueprint)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # cors
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Register apps
    initialize_errorhandlers(app)

    app.register_error_handler(400, ValidationError)

    # initialize celery
    celery_app.conf.update(app.config)

    # register celery tasks
    import celery_conf.tasks

    # bind app to db
    db.init_app(app)

    # import models
    import api.models
    # import views
    import api.views

    # initialize migration scripts
    migrate = Migrate(app, db)

    return app


@api_blueprint.errorhandler(MarshmallowError)
def handle_validation_error(error):
    """Error handler called when a ValidationError Exception is raised."""
    errors = []
    if isinstance(error.messages, dict):
        for k, v in error.messages.items():
            for error in v:
                error = error.lower()
                if k in EXCLUDED_KEYS:
                    errors.append(f'{error}')
                else:
                    errors.append(f'{k} {error}')
    else:
        errors.extend(error.messages)
    return_message = {'status': 'failed', 'errors': errors}
    return return_message, 400


@api.errorhandler(ValidationError)
@middleware_blueprint.app_errorhandler(ValidationError)
def handle_exception(error):
    """Error handler called when a ValidationError Exception is raised."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    # return response
    return error.to_dict(), error.status_code
