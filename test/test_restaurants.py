import pytest
from html import unescape

from flaskapp import create_app

from test.utilities import add_restaurant

@pytest.fixture
def client():
    app = create_app("Testing")
    
    with app.test_client() as client:
        with app.app_context():
            from flaskapp.models import Restaurant, MenuItem, db
            db.create_all()
        yield client
    
    with app.app_context():
        from flaskapp import db
        db.drop_all()
        


def test_empty_db(client):
    rv = client.get('/restaurants/json/')
    assert rv.is_json
    json_data = rv.json
    assert 'Restaurants' in json_data
    assert len(json_data['Restaurants']) == 0


def test_a_user_is_able_to_add_a_restaurant(client):
    restaurant_name = 'Mama Mia\'s😊'
    rv = add_restaurant(client, restaurant_name)
    assert unescape(rv.data.decode('utf-8')).count(restaurant_name) == 2


def test_a_newly_added_restaurant_is_visibile_in_API(client):
    restaurant_name = 'Mama Mia\'s😊'
    add_restaurant(client, restaurant_name)
    rv = client.get('/restaurants/json/')
    json_data = rv.json
    assert 'Restaurants' in json_data
    assert len(json_data['Restaurants']) == 1
    assert json_data['Restaurants'][0]['name'] == restaurant_name
    
    