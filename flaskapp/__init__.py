from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='Super_Secret_Key',
    SQLALCHEMY_DATABASE_URI='sqlite:///restaurantmenu.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

db = SQLAlchemy(app)

from flaskapp.restaurants import views
