from flask import (Flask, render_template, request,
                   redirect, url_for, flash, jsonify)
from flask_sqlalchemy import SQLAlchemy
from database_access import DBAccess


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurantmenu.db'
dbsession = DBAccess(SQLAlchemy(app))


@app.route('/')
@app.route('/restaurants/')
def restaurants():
    return render_template(
        'restaurants.html',
        restaurants=dbsession.getRestaurants())


@app.route('/restaurants/new/',
           methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        dbsession.createNewRestaurant(request.form['name'])
        flash('"%s" Created!' % request.form['name'])
        return redirect(url_for('restaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit')
def renameRestaurant(restaurant_id):
    return 'Page for creating new restaurants'


@app.route('/restaurants/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return 'Page for creating new restaurants'


@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    return render_template(
        'menu.html',
        restaurant=dbsession.getRestaurant(restaurant_id),
        items=dbsession.getMenuItems(restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        dbsession.createNewMenuItem(restaurant_id, request.form['name'])
        flash("New menu item created!")
        return redirect(url_for(
            'restaurantMenu',
            restaurant_id=restaurant_id))
    else:
        return render_template(
            'newMenuItem.html',
            restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        dbsession.editMenuItem(
            menuId=menu_id,
            name=request.form['name'])
        flash("Menu item updated!")
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    return render_template(
        'editMenuItem.html',
        menuItem=dbsession.getMenuItem(menu_id))


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        dbsession.deleteMenuItem(menuId=menu_id)
        flash("Menu item deleted!")
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    return render_template(
        'deleteMenuItem.html',
        menuItem=dbsession.getMenuItem(menu_id))


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    items = dbsession.getMenuItems(restaurant_id)
    return jsonify(MenuItems=[i.serialize() for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    menu = dbsession.getMenuItem(menu_id)
    return jsonify(MenuItem=menu.serialize())


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
