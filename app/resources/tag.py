from flask_smorest import Blueprint, abort
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from app.db import db
from app.models import *
from app.schemas import TagSchema, TagAndItemSchema

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
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(
                404,
                message="Tag already exist in this store"
            )
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(
                500,
                message=f"Something went wrong while saving tag, {e}"
            )

        return tag


@blp_tags.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp_tags.response(201, TagSchema)
    def post(self, item_id: str, tag_id: str) -> object:
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="An error occured while in linking tag with item"
            )

        return tag


    @blp_tags.response(200, TagAndItemSchema)
    def delete(self, item_id: str, tag_id: str) -> object:
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="error while deleting tag with item"
            )

        return {"message": "Item removed from tag", "item": item, "tag": tag}


@blp_tags.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp_tags.response(200, TagSchema)
    def get(self, tag_id: str) -> object:
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    def delete(self, tag_id: str) -> object:
        tag = TagModel.query.get_or_404(tag_id)

        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted"}
        abort(
            400,
            message="Could not delete tag. Make sure there is no link between tag and item"
        )
