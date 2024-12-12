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
        return {"message": f"Workout Exercise with ID {workout_exercise_id} does not exist"}, 404
    
@workout_exercises_bp.route("/", methods=["POST"])
def create_workout_exercise():
    try:
        body_data = request.get_json()

        new_workout_exercise = WorkoutExercise(
            sets=body_data.get("sets"),
            reps=body_data.get("reps"),
            weight=body_data.get("weight"),
            workout_id=body_data.get("workout_id"),
            exercise_id=body_data.get("exercise_id")
        )

        db.session.add(new_workout_exercise)

        db.session.commit()

        return workout_exercise_schema.dump(new_workout_exercise), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        
@workout_exercises_bp.route("/<int:workout_exercise_id>", methods=["DELETE"])
def delete_workout_exercise(workout_exercise_id):
    stmt = db.select(WorkoutExercise).filter_by(id=workout_exercise_id)
    workout_exercise = db.session.scalar(stmt)

    if workout_exercise:
        db.session.delete(workout_exercise)
        db.session.commit()

        return {"message": f"Workout exercise with ID {workout_exercise.id} deleted successfully."}
    else:
        return {"message": f"Workout with ID {workout_exercise_id} does not exist"}, 404
    
@workout_exercises_bp.route("/<int:workout_exercise_id>", methods=["PUT", "PATCH"])
def update_workout_exercise(workout_exercise_id):
    try:
        stmt = db.select(WorkoutExercise).filter_by(id=workout_exercise_id)
        workout_exercise = db.session.scalar(stmt)

        body_data = request.get_json()
        
        if workout_exercise:
            workout_exercise.sets = body_data.get("sets") or workout_exercise.sets
            workout_exercise.reps = body_data.get("reps") or workout_exercise.reps
            workout_exercise.weight = body_data.get("weight") or workout_exercise.weight
            workout_exercise.workout_id = body_data.get("workout_id") or workout_exercise.workout_id
            workout_exercise.exercise_id = body_data.get("exercise_id") or workout_exercise.exercise_id

            db.session.commit()

            return workout_exercise_schema.dump(workout_exercise)
        else:
            return {"message": f"Workout exercise with ID {workout_exercise_id} does not exist"}, 404
    except IntegrityError as err:
        return {"message": err.orig.diag.message_primary}, 409