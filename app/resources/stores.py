from flask_smorest import Blueprint, abort
from flask.views import MethodView
import uuid

from app.schemas import StoreSchema
from app.models import *
from app.db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

blp_store = Blueprint('stores', __name__, description="operations on stores")


@blp_store.route("/store")
class Store(MethodView):
    @blp_store.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.order_by()

    @blp_store.arguments(StoreSchema)
    @blp_store.response(200, StoreSchema)
    def post(self, request_data):
        store_init = StoreModel(**request_data)
        try:
            db.session.add(store_init)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="Store with that name already exist"
            )
        except SQLAlchemyError:
            abort(
                500,
                message="Something went wrong when inserting into store"
            )
        return store_init, 201


@blp_store.route("/store/<string:store_id>")
class StoreById(MethodView):
    @blp_store.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def post(self, store_id):
        pass

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted!"}



