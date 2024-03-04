from sqlalchemy import Column, Integer, Float, String, ForeignKey
from db import db


class ItemModel(db.Model):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    price = Column(Float(2), unique=False, nullable=False)
    store_id = Column(Integer, ForeignKey("stores.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="items")
