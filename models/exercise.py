from init import db, ma

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False, unique=True)
    muscle_group = db.Column(db.String(100), nullable=False)

class ExerciseSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "muscle_group")

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)