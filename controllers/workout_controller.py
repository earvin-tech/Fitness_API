from flask import Blueprint, request # type:ignore
from sqlalchemy.exc import IntegrityError, DataError # type:ignore
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
    
@workouts_bp.route("/", methods=["POST"])
def create_workout():
    try:
        body_data = request.get_json()

        new_workout = Workout(
            name=body_data.get("name"),
            user_id=body_data.get("user_id"),
            workout_date=body_data.get("workout_date"),
            duration=body_data.get("duration")
        )

        db.session.add(new_workout)

        db.session.commit()

        return workout_schema.dump(new_workout), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        
@workouts_bp.route("/<int:workout_id>", methods=["DELETE"])
def delete_workout(workout_id):
    stmt = db.select(Workout).filter_by(id=workout_id)
    workout = db.session.scalar(stmt)

    if workout:
        db.session.delete(workout)
        db.session.commit()

        return {"message": f"Workout with ID {workout.id} deleted successfully"}
    else:
        return {"message": f"Workout with ID {workout_id} does not exist"}, 404

@workouts_bp.route("/<int:workout_id>", methods=["PUT", "PATCH"])
def update_workout(workout_id):
    try:
        stmt = db.select(Workout).filter_by(id=workout_id)
        workout = db.session.scalar(stmt)

        body_data = request.get_json()

        if workout:
            workout.name = body_data.get("name") or workout.name
            workout.user_id = body_data.get("user_id") or workout.user_id
            workout.workout_date = body_data.get("workout_date") or workout.workout_date
            workout.duration = body_data.get("duration") or workout.duration

            db.session.commit()

            return workout_schema.dump(workout)
        else:
            return {"message": f"Workout with ID {workout_id} does not exist"}
    except DataError as err:
        return {"message": err.orig.diag.message_primary}, 409