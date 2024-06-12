from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from app.db import db
from app.models import *
from app.schemas import TagSchema

blp_tags = Blueprint("tags", __name__, description="tags for stores and item")


@blp_tags.route("/store/<string:store_id>/tag")
class TagInStore(MethodView):
    @blp_tags.response(200, TagSchema(many=True))
    def get(self, store_id: str) -> object:
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @blp_tags.arguments(TagSchema)
    @blp_tags.response(201, TagSchema)
    def post(self, tag_data, store_id: str) -> object:
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="Something went wrong while saving tag"
            )

        return tag


@blp_tags.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp_tags.response(200, TagSchema)
    def get(self, tag_id: str) -> object:
        tag = TagModel.query.get_or_404(tag_id)
        return tag


    def delete(self, tag_id: str) -> object:
        pass
