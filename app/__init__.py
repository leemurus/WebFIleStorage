import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

login_manager = LoginManager()


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    # Create folder for store
    if not os.path.isdir(app.config.get('UPLOAD_FOLDER')):
        os.mkdir(app.config.get('UPLOAD_FOLDER'))

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


from app import models, utils
