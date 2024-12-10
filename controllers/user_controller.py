from flask import Blueprint, request # type: ignore
from sqlalchemy.exc import IntegrityError # type: ignore
from psycopg2 import errorcodes # type: ignore

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

@users_bp.route("/", methods=["POST"])
def create_user():
    try: 
        body_data = request.get_json()

        new_user = User(
            f_name=body_data.get("f_name"),
            l_name=body_data.get("l_name"),
            dob=body_data.get("dob"),
            email=body_data.get("email")
        )

        db.session.add(new_user)

        db.session.commit()

        return user_schema.dump(new_user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409

        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Email address is already in use"}, 409

@users_bp.route("/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    stmt = db.select(User).filter_by(id=user_id)
    user = db.session.scalar(stmt)

    if user:
        db.session.delete(user)
        db.session.commit()

        return {"message": f"User '{user.f_name} {user.l_name}' deleted successfully"}
    else:
        return {"message": f"User with ID {user_id} does not exist"}, 404
    

@users_bp.route("/<int:user_id>", methods=["PUT", "PATCH"])
def update_user(user_id):
    try:
        stmt = db.select(User).filter_by(id=user_id)
        user = db.session.scalar(stmt)

        body_data = request.get_json()

        if user:
            user.f_name = body_data.get("f_name") or user.f_name
            user.l_name = body_data.get("l_name") or user.l_name
            user.dob = body_data.get("dob") or user.dob
            user.email = body_data.get("email") or user.email

            db.session.commit()

            return user_schema.dump(user)
        else:
            return {"message": f"User with ID {user_id} does not exist"}, 404


    except IntegrityError:
        return {"message": "Email address is already in use"}, 409