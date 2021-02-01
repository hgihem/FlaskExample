import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or 'Super_Secret_Key',
    SQLALCHEMY_TRACK_MODIFICATIONS = False,
    

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev.db')


class TestingConfig(Config):
    TESTING = True,
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db'),


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('FLASK_DB_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'dev.db')