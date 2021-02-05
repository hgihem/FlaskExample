def add_restaurant(client, restaurant_name):
    return client.post('/restaurants/new/', 
                       data=dict(name=restaurant_name),
                       follow_redirects=True)
    
