from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
db = SQLAlchemy(app)

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)

    def __repr__(self):
        return "<Restaurant(\n\tname='%s',\n\tid='%i'\n)>" % (self.name, self.id)


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable = False)
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)

    def serialize(self):
        return {
            'name'          :self.name,
            'description'   :self.description,
            'id'            :self.id,
            'price'         :self.price,
            'course'        :self.course,
        }

    def __repr__(self):
        return "<MenuItem(\n\tname='%s',\n\tid='%i',\n\tcourse='%s',\n\tdescription='%s',\n\tprice='%s',\n\trestaurant_id='%s'\n)>" % (
            self.name, self.id, self.course, self.description, self.price, self.restaurant_id)


db.create_all()
