from app import app
from flask import render_template, request


@app.route('/')
def hello_world():
    return render_template('index.html')


stores = [
    {
        "name": 'aidin',
        'items': [
            {
                'name': 'milk',
                'price': 200,
            },
            {
                'name': 'water',
                'price': 10
            }
        ]
    }
]


@app.get('/store')
def get_score():
    return stores


@app.post('/store')
def add_new_store():
    request_data = request.get_json()
    new_store = {'name': request_data['name'], 'items': []}
    stores.append(new_store)
    return new_store, 201


@app.post('/store/<string:name>/item')
def add_items(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_items = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_items)
            return new_items, 201
    return {'message': 'store not found'}, 404


@app.get('/store/<string:name>/item')
def get_items(name):
    for store in stores:
        if store['name'] == name:
            return store['items'], 200
    return {'message': 'store not found'}, 404

