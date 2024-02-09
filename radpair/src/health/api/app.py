import logging
from flask import Blueprint, Flask
from flask_cors import CORS
from werkzeug.utils import find_modules, import_string

from radpair.src.health.api.services.context_manager import ( ContextManager)
from .config import FlaskAppConfig
from .extensions import jwt_configuration


def register_blueprints(import_name: str, app: Flask) -> None:
    try:
        for name in find_modules(import_name, recursive=True):
            mod = import_string(name)
            blueprints = [b for b in mod.__dict__.values() if isinstance(b, Blueprint)]
            for blueprint in blueprints:
                app.register_blueprint(blueprint)
                logging.info("%s: blueprint loaded")
    except Exception as e:
        logging.exception("Unable to load blueprints exception raised:{}".format(e))
        raise e


def init_context_manager():
    """
    initializes the context manager as a runtime helper service
    Raises:
        RuntimeError: rasied if the system is unable to initialize the context manager
    """
    try:
        ContextManager().register()
    except OSError:
        logging.exception("Something went wrong during environment registration.")
        raise RuntimeError("Unable to setup runtime environment!")


def init_authetication(app: Flask) -> None:
    """Init extensions for a flask app"""
    jwt_configuration.init_jwt_auth(app)

def init_database(app: Flask) -> None:
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking for efficiency
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'


def create_app(
    import_name: str,
    autoload_blueprints: bool = True,
    blueprints_module: str = "blueprints",
) -> Flask:
    # 2 instances cause of debugging
    init_context_manager()
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(FlaskAppConfig)
    app.config["MAX_CONTENT_LENGTH"] = 1073741824 # this is not required for the radpair demo but, it can be adjusted if we were sending media i.e a mp4 or mp3 voice upload
    if autoload_blueprints:
        register_blueprints(f"{import_name}.{blueprints_module}", app)
    init_authetication(app)
    return app
