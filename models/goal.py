from marshmallow import fields # type:ignore

from init import db, ma

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    goal_weight = db.Column(db.Float, nullable=False)
    status_achieved = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="goals")
    exercise = db.relationship("Exercise", back_populates="goals")
    
class GoalSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["f_name", "l_name"])
    exercise = fields.Nested("ExerciseSchema", only=["name"])
    class Meta:
        fields = ("id", "name", "exercise_id", "user_id", "goal_weight", "status_achiieved", "user", "exercise")

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)