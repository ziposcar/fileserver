from flask import Flask
from config import current_config
from views import main

def create_app(config_name):
    blueprints = [main, ]

    # current_config = config_name
    app = Flask(__name__, static_folder=current_config['static_folder'])
    app.config.from_object(current_config)
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    return app
