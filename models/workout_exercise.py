from marshmallow import fields # type:ignore

from init import db, ma

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    sets = db.Column(db.Integer, nullable=False, default=1)
    reps = db.Column(db.Integer, nullable=False, default=1)
    weight = db.Column(db.Float, nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

class WorkoutExerciseSchema(ma.Schema):
    workout = fields.Nested("WorkoutSchema", only=["user_id","name"])
    exercise = fields.Nested("ExerciseSchema", only=["name"])
    class Meta:
        fields = ("id", "sets", "reps", "weight", "workout_id", "exercise_id", "workout", "exercise") 

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)