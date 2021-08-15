import os

basedir = os.path.dirname(os.path.realpath(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'the hardest secret key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
