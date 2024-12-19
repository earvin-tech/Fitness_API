from marshmallow import fields, validates # type: ignore
from marshmallow.validate import Regexp, And, Length # type: ignore
from marshmallow.exceptions import ValidationError  # type: ignore

from init import db, ma

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group = db.Column(db.String(100), nullable=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all,delete")
    goals = db.relationship("Goal", back_populates="exercise", cascade="all,delete")

class ExerciseSchema(ma.Schema):
    name = fields.String(required=True, validate = And(
        Regexp('^[A-Za-z][A-Za-z]*$', error="Only letters are allowed"),
        Length(min=2, error="Name must be at least 2 characters long")
    ))

    muscle_group = fields.String(validate = And(
        Regexp('^[A-Za-z][A-Za-z]*$', error="Only letters are allowed"),
        Length(min=2, error="Muscle group must be at least 2 characters long")
    ))

    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=["exercise"]))
    goals = fields.List(fields.Nested("GoalSchema", exclude=["exercise"]))
    class Meta:
        fields = ("id", "name", "muscle_group", "workout_exercises", "goals")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)