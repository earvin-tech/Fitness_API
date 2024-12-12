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