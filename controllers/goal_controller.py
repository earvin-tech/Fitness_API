from flask import Blueprint, request # type:ignore
from sqlalchemy.exc import IntegrityError, DataError # type:ignore
from psycopg2 import errorcodes # type:ignore

from init import db
from models.goal import Goal, goal_schema, goals_schema

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("/")
def get_goals():
    stmt = db.select(Goal)
    goals_list = db.session.scalars(stmt)
    data = goals_schema.dump(goals_list)
    return data

@goals_bp.route("/<int:goal_id>")
def get_goal(goal_id):
    stmt = db.select(Goal).filter_by(id=goal_id)
    goal = db.session.scalar(stmt)
    if goal:
        data = goal_schema.dump(goal)
        return data
    else:
        return {"message": f"Goal with ID {goal_id} does not exist"}, 404
    
@goals_bp.route("/", methods=["POST"])
def create_goal():
    try:
        body_data = request.get_json()

        new_goal = Goal(
            name=body_data.get("name"),
            exercise_id=body_data.get("exercise_id"),
            user_id=body_data.get("user_id"),
            goal_weight=body_data.get("goal_weight"),
            status_achieved=body_data.get("status_achieved")
        )

        db.session.add(new_goal)

        db.session.commit()

        return goal_schema.dump(new_goal), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409