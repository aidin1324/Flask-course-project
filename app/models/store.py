from app.db import db


class StoreModel(db.Model):
    __tablename__ = 'Stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)