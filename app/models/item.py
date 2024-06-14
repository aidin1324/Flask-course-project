from app.db import db


class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), unique=False, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    item_tag = db.relationship("TagModel", back_populates="items", secondary="itemtag" )