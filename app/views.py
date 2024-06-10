import uuid

from app import app
from flask import render_template, request
from .db import stores, items
from flask_smorest import abort
@app.route('/')
def hello_world():
    return render_template('index.html')



@app.get("/store")
def get_stores():
    return {'stores': list(stores.values())}


@app.get('/store/<string:store_id>')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return abort(404, message='store Not found')


@app.post('/store')
def add_new_store():
    request_data = request.get_json()

    if "name" not in request_data:
        abort(
            404, message="Bad request: missing 'name'"
        )
    for store in stores.values():
        if request_data["name"] == store["name"]:
            abort(
                400, message="Bad request: store already exist"
            )
    store_id = uuid.uuid4().hex
    store = {**request_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post('/item')
def add_items():
    item_data = request.get_json()

    if (
        'price' not in item_data
        or 'store_id' not in item_data
        or 'name' not in item_data
    ):
        abort(
            400,
            message="Bad request. Ensure 'price, 'store_id' and 'name' are included in the JSON"
        )
    if item_data['store_id'] not in stores:
        return abort(404, message='store Not found')

    for item in items.values():
        if (
            item["store_id"] == item_data['store_id']
            and item["name"] == item_data['name']
        ):
            abort(400, message="Item already exists")

    if item_data['store_id'] not in stores:
        abort(
            404, message="Store Not found"
        )

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


@app.get("/item")
def get_all_items():
    return {'items': list(items.values())}


@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return abort(404, message='item Not found')

