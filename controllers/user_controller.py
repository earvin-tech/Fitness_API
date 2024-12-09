from flask import Blueprint # type: ignore

from init import db
from models.user import User, users_schema, user_schema

users_bp = Blueprint("users", __name__, url_prefix="/users")

@users_bp.route("/")
def get_users():
    stmt = db.select(User)
    users_list = db.session.scalars(stmt)
    data = users_schema.dump(users_list)
    return data

@users_bp.route("/<int:user_id>")
def get_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)
    if user:
        data = user_schema.dump(user)
        return data
    else:
        return {"message": f"User with ID {user_id} does not exist"}, 404