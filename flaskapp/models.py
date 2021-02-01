from flaskapp import db

class Restaurant(db.Model):
    __tablename__ = 'restaurant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    
    def serialize(self):
        return {
            'name':         self.name,
            'id':           self.id,
        }

    def __repr__(self):
        return f'<Restaurant(\n\tname=\'{self.name}\',\n\tid=\'{self.id}\'\n)>'


class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    course = db.Column(db.String(250))
    description = db.Column(db.String(250))
    price = db.Column(db.String(8))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    restaurant = db.relationship(Restaurant)

    def serialize(self):
        return {
            'name':         self.name,
            'description':  self.description,
            'id':           self.id,
            'price':        self.price,
            'course':       self.course,
        }

    def __repr__(self):
        return f'<MenuItem(\n\tname=\'{self.name}\',\n\tid=\'{self.id}\','              \
            '\n\tcourse=\'{self.course}\',\n\tdescription=\'{self.description}\','      \
            '\n\tprice=\'{self.price}\',\n\trestaurant_id=\'{self.restaurant_id}\'\n)>'


Courses = {'Appetizer': 0, 'Entree': 1, 'Dessert': 2}
