from db import db
from sqlalchemy import Column, Integer, String


class UserModel(db.Model):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, unique=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
