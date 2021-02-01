from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config


db = SQLAlchemy()


def create_app(config_env=""):
    app = Flask(__name__)
    if not config_env:
        config_env = app.env
    app.config.from_object(f'config.{config_env.capitalize()}Config')

    db.init_app(app)

    from flaskapp.restaurants.views import restaurants
    app.register_blueprint(restaurants, url_prefix='/restaurants')
    
    return app
