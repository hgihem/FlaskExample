from sqlalchemy import case
from flaskapp.models import Restaurant, MenuItem, Courses
from flaskapp import db


class DBAccess:
    @staticmethod
    def getRestaurant(restaurantId: int) -> Restaurant:
        return db.session.query(Restaurant) \
            .filter_by(id=restaurantId).first()

    @staticmethod
    def getMenuItem(menuId: int) -> MenuItem:
        return db.session.query(MenuItem).filter_by(id=menuId).first()

    @staticmethod
    def getRestaurants():
        return db.session.query(Restaurant).order_by(Restaurant.name)
    
    @staticmethod
    def getCourses(restaurantId: int):
        sort_order = case(value=MenuItem.course, whens=Courses)
        return db.session.query(MenuItem.course).distinct().filter_by(
            restaurant_id=restaurantId).order_by(sort_order)

    @staticmethod
    def getMenuItems(restaurantId: int):
        return db.session.query(MenuItem).filter_by(
            restaurant_id=restaurantId)

    @staticmethod
    def getMenuItemsByCourse(restaurantId: int):
        return [(course[0], db.session.query(MenuItem).filter_by(
                                restaurant_id=restaurantId,
                                course=course[0]))
                for course
                in DBAccess.getCourses(restaurantId)]

    @staticmethod
    def createNewRestaurant(name: str):
        new_restaurant = Restaurant(
            name=name)
        db.session.add(new_restaurant)
        db.session.commit()

    @staticmethod
    def createNewMenuItem(restaurantId: int,
                          name:         str,
                          price:        str,
                          description:  str,
                          course:       str):
        new_menu_item = MenuItem(
            name=name,
            price=price,
            description=description,
            restaurant_id=restaurantId,
            course=course,
            )
        db.session.add(new_menu_item)
        db.session.commit()

    @staticmethod
    def renameRestaurant(restaurantId: int, name: str):
        restaurant = DBAccess.getRestaurant(restaurantId)
        restaurant.name = name
        db.session.commit()

    @staticmethod
    def editMenuItem(menuId:        int,
                     name:          str,
                     price:         str,
                     description:   str,
                     course:        str):
        menu_item = DBAccess.getMenuItem(menuId=menuId)
        menu_item.name = name
        menu_item.price = price
        menu_item.description = description
        menu_item.course = course
        db.session.commit()

    @staticmethod
    def deleteRestaurant(restaurantId: int):
        db.session.delete(DBAccess.getRestaurant(restaurantId))
        db.session.commit()

    @staticmethod
    def deleteMenuItem(menuId: int):
        db.session.delete(DBAccess.getMenuItem(menuId=menuId))
        db.session.commit()
