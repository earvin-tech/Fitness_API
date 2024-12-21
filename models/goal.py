from marshmallow import fields, validates # type:ignore
from marshmallow.validate import Length, And, Regexp # type: ignore
from marshmallow.exceptions import ValidationError # type: ignore



from init import db, ma

class Goal(db.Model):
    __tablename__ = "goals"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    goal_weight = db.Column(db.Float, nullable=False)
    target_date = db.Column(db.Date)
    status_achieved = db.Column(db.Boolean, nullable=False, default=False)

    user = db.relationship("User", back_populates="goals")
    exercise = db.relationship("Exercise", back_populates="goals")
    
class GoalSchema(ma.Schema):

    name = fields.String(validate=And(
        Length(min=2, error="Name must be at least 2 characters long"),
        Regexp('^[A-Za-z][A-Za-z0-9 ]*$', error="Only alphanumeric characters and spaces allowed, eg: 'Stronger Legs'")
    ))

    @validates('goal_weight')
    def validate_goal_weight(self, value):
        if value < 0.25:
            raise ValidationError("Goal weight must be at least 0.25 kgs ")

    user = fields.Nested("UserSchema", only=["f_name", "l_name"])
    exercise = fields.Nested("ExerciseSchema", only=["name"])
    class Meta:
        fields = ("id", "name", "exercise_id", "user_id", "goal_weight", "status_achieved", "target_date", "user", "exercise")

goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)