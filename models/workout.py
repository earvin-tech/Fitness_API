from marshmallow import fields, validates # type:ignore
from datetime import date
from marshmallow.validate import And, Regexp # type: ignore
from marshmallow.exceptions import ValidationError # type:ignore

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
    @validates('workout_date')
    def validate_workout_date(self, value):
        today = date.today()
        if date.fromisoformat(value) < date.fromisoformat("2010-01-01"):
            raise ValidationError("Workout date cannot be before Jan 1st 2010")
        if date.fromisoformat(value) > today:
            raise ValidationError("Workout date cannot be in the future")
        
    @validates('duration')
    def validate_duration(self, value):
        if value > "24:00:00":
            raise ValidationError("Duration cannot be longer than 24 hours")
        
    name = fields.String(validate=And(
        Regexp('^[A-Za-z][A-Za-z0-9 ]*$', error="Only alphanumeric characters and spaces allowed, eg: 'Arm Workout 7'")
    ))

    ordered=True
    user = fields.Nested("UserSchema", only=["f_name", "l_name"])
    workout_exercises = fields.List(fields.Nested("WorkoutExerciseSchema", exclude=["workout"]))
    class Meta:
        fields = ("id", "name", "user_id", "workout_date", "duration", "user", "workout_exercises")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)