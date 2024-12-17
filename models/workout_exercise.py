from marshmallow import fields, validates # type:ignore
from marshmallow.exceptions import ValidationError # type: ignore


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
    
    @validates('sets')
    def validate_sets(self, value):
        if value < 1:
            raise ValidationError("Sets cannot be less than 1")
        
    @validates('reps')
    def validate_reps(self, value):
        if value < 1:
            raise ValidationError("Reps cannot be less than 1")
        
    @validates('weight')
    def validate_weight(self, value):
        if value < 0.25:
            raise ValidationError("Weight must be at least 0.25 kgs")

    workout = fields.Nested("WorkoutSchema", only=["user_id","name"])
    exercise = fields.Nested("ExerciseSchema", only=["name"])
    class Meta:
        fields = ("id", "sets", "reps", "weight", "workout_id", "exercise_id", "workout", "exercise") 

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)