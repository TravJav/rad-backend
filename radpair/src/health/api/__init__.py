from .app import create_app

app = create_app(__name__, autoload_blueprints=True, blueprints_module="blueprints")