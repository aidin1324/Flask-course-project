from flask_smorest import Blueprint, abort
from flask.views import MethodView
import uuid
from flask import request
from app.db import items, stores


blp_store = Blueprint('stores', __name__, description="operations on stores")


@blp_store.route("/store")
class Store(MethodView):
    def get(self):
        return {'stores': list(stores.values())}

    def post(self):
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


@blp.route("/store/<string: store_id>")
class StoreById(MethodView):
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



