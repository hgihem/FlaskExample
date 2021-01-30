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
        flash(f'"{request.form["name"]}" Created!')
        return redirect(url_for('restaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit',
           methods=['GET', 'POST'])
def renameRestaurant(restaurant_id):
    if request.method == 'POST':
        dbsession.renameRestaurant(
            restaurantId=restaurant_id,
            name=request.form['name'])
        flash(f'Restaurant "{request.form["name"]}" Renamed!')
        return redirect(url_for('restaurants'))
    else:
        return render_template(
            'editRestaurant.html',
            restaurant=dbsession.getRestaurant(restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/delete',
           methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        name = dbsession.getRestaurant(restaurant_id).name
        dbsession.deleteRestaurant(restaurant_id)
        flash(f'Removed "{name}"!')
        return redirect(url_for('restaurants'))
    return render_template(
            'deleteRestaurant.html',
            restaurant=dbsession.getRestaurant(restaurant_id))


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
        dbsession.createNewMenuItem(
            restaurantId=restaurant_id,
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'])
        flash(f'"{request.form["name"]}" created!')
        return redirect(url_for(
            'restaurantMenu',
            restaurant_id=restaurant_id))
    else:
        return render_template(
            'newMenuItem.html',
            restaurant=dbsession.getRestaurant(restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        dbsession.editMenuItem(
            menuId=menu_id,
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'])
        flash(f'{request.form["name"]} updated!')
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
        flash('Menu item deleted!')
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
def restaurantMenuItemJSON(menu_id):
    menu = dbsession.getMenuItem(menu_id)
    return jsonify(MenuItem=menu.serialize())


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
