import os

from flask import Flask

from crossgameflask.application.controllers import controller_game
from crossgameflask.application.controllers import controller_index
from crossgameflask.application.errors.error_handlers import internal_error, page_not_found
from crossgameflask.application.errors.exceptions import AttributeIsNotFoundInTheFormException, IncorrectStringValue, \
    NoUserInTheSession


def configure_flask_app(application: Flask, test_config=None):
    key: str = os.environ['FLASK_APP_KEY']
    app_key = key if key and len(key) > 0 else 'development_key_tmp'

    application.config.from_mapping(
        SECRET_KEY=app_key
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application.config.from_mapping(test_config)
    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass
    application.register_blueprint(controller_index.INDEX_BLUEPRINT)
    application.register_blueprint(controller_game.GAME_BLUEPRINT)
    application.register_error_handler(400, page_not_found)
    application.register_error_handler(500, internal_error)
    application.register_error_handler(AttributeIsNotFoundInTheFormException, internal_error)
    application.register_error_handler(NoUserInTheSession, internal_error)
    application.register_error_handler(IncorrectStringValue, internal_error)
