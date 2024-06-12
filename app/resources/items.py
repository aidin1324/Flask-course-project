from flask.views import MethodView
from flask_smorest import Blueprint, abort

import uuid

from sqlalchemy.exc import SQLAlchemyError

from app.schemas import ItemSchema, ItemUpdateSchema
from app.db import db
from app.models import *

blp_items = Blueprint('items', __name__, description="operations on item")


@blp_items.route('/item')
class Item(MethodView):
    @blp_items.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.order_by()

    @blp_items.arguments(ItemSchema)
    @blp_items.response(201, ItemSchema)
    def post(self, item_data):
        item_init = ItemModel(**item_data)
        try:
            db.session.add(item_init)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="An error occurred"
            )

        return item_init, 201


@blp_items.route('/item/<string:item_id>')
class Itemid(MethodView):
    @blp_items.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted!"}

    @blp_items.arguments(ItemUpdateSchema)
    @blp_items.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            if "name" in item_data:
                item.name = item_data['name']
            if "price" in item_data:
                item.price = item_data['price']
        else:
            item = ItemModel(id=item_id,**item_data)

        db.session.add(item)
        db.session.commit()

        return item
