from flask import Blueprint, request # type: ignore
from sqlalchemy.exc import IntegrityError # type:ignore
from psycopg2 import errorcodes # type:ignore

from init import db
from models.workout_exercise import WorkoutExercise, workout_exercise_schema, workout_exercises_schema

workout_exercises_bp = Blueprint("workout_exercises", __name__, url_prefix="/workout_exercises")

@workout_exercises_bp.route("/")
def get_workout_exercises():
    stmt = db.select(WorkoutExercise)
    workout_exercises_list = db.session.scalars(stmt)
    data = workout_exercises_schema.dump(workout_exercises_list)
    return data

@workout_exercises_bp.route("/<int:workout_exercise_id>")
def get_workout_exercise(workout_exercise_id):
    stmt = db.select(WorkoutExercise).filter_by(id=workout_exercise_id)
    workout_exercise = db.session.scalar(stmt)

    if workout_exercise:
        data = workout_exercise_schema.dump(workout_exercise)
        return data
    else:
        return {"message": f"Workout Exercise with ID {workout_exercise_id} does not exist"}