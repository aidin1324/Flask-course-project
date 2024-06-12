from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

import uuid
from app.db import stores, items
from app.schemas import ItemSchema, ItemUpdateSchema
blp_items = Blueprint('items', __name__, description="operations on item")


@blp_items.route('/item')
class Item(MethodView):
    @blp_items.response(200, ItemSchema(many=True))
    def get(self):
        return {'items': list(items.values())}

    @blp_items.arguments(ItemSchema)
    @blp_items.response(200, ItemSchema)
    def post(self, item_data):

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
    @blp_items.response(200, ItemSchema)
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

    @blp_items.arguments(ItemUpdateSchema)
    @blp_items.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            return abort(
                404,
                message="Item not found"
            )
