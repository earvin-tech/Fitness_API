from init import db, ma

class Workout(db.model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    workout_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.Interval, nullable=False)

class WorkoutSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "workout_date", "duration")

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)