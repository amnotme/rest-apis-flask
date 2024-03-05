from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from db import db
from models import UserModel
from schemas import UserSchema
from flask_jwt_extended import create_access_token, create_refresh_token


blp = Blueprint("users", __name__, description="Operations for users")


@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(status_code=200, schema=UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

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
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        abort(http_status_code=401, message="Invalid username or password provided.")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(schema=UserSchema)
    def post(self, user_data):

        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(http_status_code=409, message="Username already taken")

        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                http_status_code=500,
                message="something occurred while creating user. Please try again.",
            )

        return {"message": "User has been successfully created."}, 201
