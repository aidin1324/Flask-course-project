from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

import uuid
from app.db import stores, items

blp_items = Blueprint('items', __name__, description="operations on item")


@blp_items.route('/item')
class Item(MethodView):
    def get(self):
        return {'items': list(items.values())}

    def post(self):
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


@blp_items.route('/item/<string:item_id>')
class Itemid(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message='item Not found')

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "item deleted"}
        except KeyError:
            return abort(
                404,
                message="Item not found"
            )

    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            return abort(
                400,
                message="Bad request, add name or price"
            )

        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            return abort(
                404,
                message="Item not found"
            )
