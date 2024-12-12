from marshmallow import fields # type:ignore

from init import db, ma

class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    workout_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Interval, nullable=False)

    user = db.relationship("User", back_populates="workouts")
    workout_exercises = db.relationship("WorkoutExercise", back_populates="workout", cascade="all,delete")

class WorkoutSchema(ma.Schema):
    ordered=True
    user = fields.Nested("UserSchema", only=["f_name", "l_name"])
    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=["workout"]))
    class Meta:
        fields = ("id", "name", "user_id", "workout_date", "duration", "user", "workout_exercises")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)