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
        body_data = goal_schema.load(request.get_json())

        new_goal = Goal(
            name=body_data.get("name"),
            exercise_id=body_data.get("exercise_id"),
            user_id=body_data.get("user_id"),
            goal_weight=body_data.get("goal_weight"),
            target_date=body_data.get("target_date"),
            status_achieved=body_data.get("status_achieved")
        )

        db.session.add(new_goal)

        db.session.commit()

        return goal_schema.dump(new_goal), 201

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            return {"message": "Either user id or exercise id is not found"}
        
@goals_bp.route("/<int:goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    stmt = db.select(Goal).filter_by(id=goal_id)
    goal = db.session.scalar(stmt)
    if goal:
        db.session.delete(goal)
        db.session.commit()

        return {"message": f"Goal with ID {goal.id} deleted successfully"}
    else:
        return {"message": f"Goal with ID {goal_id} does not exist"}, 404
    
@goals_bp.route("/<int:goal_id>", methods=["PUT", "PATCH"])
def update_goal(goal_id):
    try:
        stmt = db.select(Goal).filter_by(id=goal_id)
        goal = db.session.scalar(stmt)

        body_data = goal_schema.load(request.get_json())

        if goal:
            goal.name = body_data.get("name") or goal.name
            goal.exercise_id = body_data.get("exercise_id") or goal.exercise_id
            goal.user_id = body_data.get("user_id") or goal.user_id
            goal.goal_weight = body_data.get("goal_weight") or goal.goal_weight
            goal.status_achieved = body_data.get("status_achieved") or goal.status_achieved
            goal.target_date = body_data.get("target_date") or goal.target_date

            db.session.commit()

            return goal_schema.dump(goal)
        else:
            return {"message": f"Goal with ID {goal_id} does not exist"}, 404

    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            return {"message": "Either user id or exercise id is not found"}
        else:
            return {"message": err.orig.diag.message_primary}, 409