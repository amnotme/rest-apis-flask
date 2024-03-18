import os

from flask.views import MethodView
from sqlalchemy import or_
from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from db import db
from models import UserModel
from schemas import UserSchema, UserRegisterSchema
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from blocklist import BLOCKLIST
from tasks import send_user_registration_email

blp = Blueprint("users", __name__, description="Operations for users")


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @jwt_required()
    @blp.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required(fresh=True)
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        try:
            db.session.delete(user)
            db.session.commit()

        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message="Something went wrong when retrieving user",
            )
        return {"message": f"User {user_id} has been deleted."}


@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(schema=UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}
        abort(http_status_code=401, message="Invalid username or password provided.")


@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        BLOCKLIST.add(get_jwt()["jti"])
        return {"message": "Successfully logged out"}, 200


@blp.route("/refresh")
class TokenRefresh(MethodView):

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token", new_token}


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(schema=UserRegisterSchema)
    def post(self, user_data):

        if UserModel.query.filter(
            or_(
                UserModel.username == user_data["username"],
                UserModel.email == user_data["email"],
            )
        ).first():
            abort(http_status_code=409, message="Username or email already taken")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
            email=user_data["email"],
        )

        try:
            db.session.add(user)
            db.session.commit()

            current_app.queue.enqueue(
                "tasks.send_user_registration_email",
                email=user.email,
                username=user.username,
            )

        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message="something occurred while creating user. Please try again.",
            )

        return {"message": "User has been successfully created."}, 201
