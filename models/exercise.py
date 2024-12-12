from marshmallow import fields # type: ignore

from init import db, ma

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group = db.Column(db.String(100), nullable=False)

    workout_exercises = db.relationship("WorkoutExercise", back_populates="exercise", cascade="all,delete")

class ExerciseSchema(ma.Schema):
    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=["exercise"]))
    class Meta:
        fields = ("id", "name", "muscle_group", "workout_exercises")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)