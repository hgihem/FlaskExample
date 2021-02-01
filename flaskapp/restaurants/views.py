from flask import render_template, request, url_for, jsonify, flash, redirect
from flaskapp import app
from flaskapp.database_access import DBAccess
from flaskapp.models import Courses

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    return render_template(
        'restaurants.html',
        restaurants=DBAccess.getRestaurants())


@app.route('/restaurants/new/',
           methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        DBAccess.createNewRestaurant(request.form['name'])
        flash(f'"{request.form["name"]}" Created!')
        return redirect(url_for('restaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit',
           methods=['GET', 'POST'])
def renameRestaurant(restaurant_id):
    if request.method == 'POST':
        DBAccess.renameRestaurant(
            restaurantId=restaurant_id,
            name=request.form['name'])
        flash(f'Restaurant "{request.form["name"]}" Renamed!')
        return redirect(url_for('restaurants'))
    else:
        return render_template(
            'editRestaurant.html',
            restaurant=DBAccess.getRestaurant(restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/delete',
           methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        name = DBAccess.getRestaurant(restaurant_id).name
        DBAccess.deleteRestaurant(restaurant_id)
        flash(f'Removed "{name}"!')
        return redirect(url_for('restaurants'))
    return render_template(
            'deleteRestaurant.html',
            restaurant=DBAccess.getRestaurant(restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    return render_template(
        'menu.html',
        restaurant=DBAccess.getRestaurant(restaurant_id),
        items=DBAccess.getMenuItemsByCourse(restaurant_id))


@app.route('/restaurants/<int:restaurant_id>/menu/new/',
           methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        DBAccess.createNewMenuItem(
            restaurantId=restaurant_id,
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'],
            course=request.form['course'])
        flash(f'"{request.form["name"]}" created!')
        return redirect(url_for(
            'restaurantMenu',
            restaurant_id=restaurant_id))
    else:
        return render_template(
            'newMenuItem.html',
            restaurant=DBAccess.getRestaurant(restaurant_id),
            courses=Courses)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        DBAccess.editMenuItem(
            menuId=menu_id,
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'],
            course=request.form['course'])
        flash(f'{request.form["name"]} updated!')
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    else:
        return render_template(
            'editMenuItem.html',
            menuItem=DBAccess.getMenuItem(menu_id),
            courses=Courses)


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        name = DBAccess.getMenuItem(menuId=menu_id)
        DBAccess.deleteMenuItem(menuId=menu_id)
        flash(f'{name} deleted!')
        return redirect(url_for('restaurantMenu',
                                restaurant_id=restaurant_id))
    return render_template(
        'deleteMenuItem.html',
        menuItem=DBAccess.getMenuItem(menu_id))


@app.route('/restaurants/JSON/')
def restaurantsJSON():
    items = DBAccess.getRestaurants()
    return jsonify(Restaurants=[i.serialize() for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    items = DBAccess.getMenuItems(restaurant_id)
    return jsonify(MenuItems=[i.serialize() for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(menu_id):
    menu = DBAccess.getMenuItem(menu_id)
    return jsonify(MenuItem=menu.serialize())
