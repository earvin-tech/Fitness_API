from flask import Blueprint, request # type: ignore
from sqlalchemy.exc import IntegrityError # type: ignore
from psycopg2 import errorcodes # type: ignore

from init import db
from models.exercise import Exercise, exercise_schema, exercises_schema

exercises_bp = Blueprint("exercises", __name__, url_prefix="/exercises")

@exercises_bp.route("/")
def get_exercises():
    stmt = db.select(Exercise)
    exercises_list = db.session.scalars(stmt)
    data = exercises_schema.dump(exercises_list)
    return data

@exercises_bp.route("/<int:exercise_id>")
def get_exercise(exercise_id):
    stmt = db.select(Exercise).filter_by(id=exercise_id)
    exercise = db.session.scalar(stmt)
    if exercise:
        data = exercise_schema.dump(exercise)
        return data
    else:
        return {"message": f"Exercise with ID {exercise_id} does not exist"}, 404