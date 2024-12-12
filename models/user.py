from marshmallow import fields # type:ignore

from init import db, ma

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    f_name = db.Column(db.String(100), nullable=False)
    l_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

    workouts = db.relationship("Workout", back_populates="user")
    goals = db.relationship("Goal", back_populates="user")

class UserSchema(ma.Schema):
    workouts = fields.List(fields.Nested("WorkoutSchema", exclude=["user"]))
    goals = fields.List(fields.Nested("GoalSchema", exclude=["user"]))
    class Meta:
        fields = ("id","f_name", "l_name", "dob", "email", "workouts", "goals")

user_schema = UserSchema()
users_schema = UserSchema(many=True)
