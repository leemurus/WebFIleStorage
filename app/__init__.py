from config import config
from flask import Flask


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
