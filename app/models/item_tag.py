from app.db import db


class ItemTagModel(db.Model):
    __tablename__ = "itemtag"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), nullable=False)

    items = db.relationship('items', back_populates='itemtag')
    tags = db.relationship('tags', back_populates='itemtag')