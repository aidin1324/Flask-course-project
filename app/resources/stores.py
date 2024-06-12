from flask_smorest import Blueprint, abort
from flask.views import MethodView
import uuid
from flask import request

from app.db import items, stores
from app.schemas import StoreSchema

blp_store = Blueprint('stores', __name__, description="operations on stores")


@blp_store.route("/store")
class Store(MethodView):
    @blp_store.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp_store.arguments(StoreSchema)
    @blp_store.response(200, StoreSchema)
    def post(self, request_data):
        for store in stores.values():
            if request_data["name"] == store["name"]:
                abort(
                    400, message="Bad request: store already exist"
                )
        store_id = uuid.uuid4().hex
        store = {**request_data, "id": store_id}
        stores[store_id] = store
        return store, 201


@blp_store.route("/store/<string:store_id>")
class StoreById(MethodView):
    @blp_store.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            return abort(404, message='store Not found')

    def post(self, store_id):
        pass

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "store successfully deleted"}
        except KeyError:
            abort(
                404,
                message="store not found"
            )



