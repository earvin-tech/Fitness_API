from flask import Blueprint, request # type:ignore
from sqlalchemy.exc import IntegrityError # type:ignore
from psycopg2 import errorcodes # type:ignore

from init import db
from models.workout import Workout, workout_schema, workouts_schema

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")

@workouts_bp.route("/")
def get_workouts():
    stmt = db.select(Workout)
    workouts_list = db.session.scalars(stmt)
    data = workouts_schema.dump(workouts_list)
    return data

@workouts_bp.route("/<int:workout_id>")
def get_workout(workout_id):
    stmt = db.select(Workout).filter_by(id=workout_id)
    workout = db.session.scalar(stmt)
    if workout:
        data = workout_schema.dump(workout)
        return data
    else:
        return {"message": f"Workout with ID {workout_id} does not exist"}, 404
