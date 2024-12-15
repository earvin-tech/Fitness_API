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
    
@exercises_bp.route("/", methods=["POST"])
def create_exercise():
    try:
        body_data = exercise_schema.load(request.get_json())

        new_exercise = Exercise(
            name=body_data.get("name"),
            muscle_group=body_data.get("muscle_group")
        )

        db.session.add(new_exercise)

        db.session.commit()

        return exercise_schema.dump(new_exercise), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Exercise name is already in use"}, 409

@exercises_bp.route("/<int:exercise_id>", methods=["DELETE"])
def delete_exercise(exercise_id):
    stmt = db.select(Exercise).filter_by(id=exercise_id)
    exercise = db.session.scalar(stmt)

    if exercise:
        db.session.delete(exercise)
        db.session.commit()

        return {"message": f"Exercise: {exercise.name} has been deleted successfully"}
    else:
        return {"message": f"Exercise with ID {exercise_id} does not exist"}, 404
    
@exercises_bp.route("/<int:exercise_id>", methods=["PUT", "PATCH"])
def update_exercise(exercise_id):
    try:
        stmt = db.select(Exercise).filter_by(id=exercise_id)
        exercise = db.session.scalar(stmt)

        body_data = exercise_schema.load(request.get_json())

        if exercise:
            exercise.name = body_data.get("name") or exercise.name
            exercise.muscle_group = body_data.get("muscle_group") or exercise.muscle_group

            db.session.commit()

            return exercise_schema.dump(exercise)
        else:
            return {"message": f"Exercise with ID {exercise_id} does not exist"}, 404

    except IntegrityError:
        return {"message": "Name of exercise is already in use"}, 409