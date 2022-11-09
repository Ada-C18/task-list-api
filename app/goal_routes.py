from app import db
from app.models.goal import Goal
from app.models.task import Task
from .route_helpers import validate_model
from flask import Blueprint, jsonify, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
# Creates a new goal and returns it as json
def create_new_goal():
    request_body = request.get_json()
    if "title" in request_body:
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()
        return {"goal": new_goal.as_dict()}, 201
    else:
        return {"details": "Invalid data"}, 400

@goals_bp.route("", methods=["GET"])
# Get every goal in the goals list
def get_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.as_dict() for goal in goals]
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
# Get one specific goal from the goals list
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.as_dict()}, 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
# Updates specified goal's name, description, and completion
def update_goal(goal_id):
    request_body = request.get_json()
    goal = validate_model(Goal, goal_id)

    if "title" in request_body:
        goal.title = request_body["title"]
        
        db.session.commit()
        return {"goal": goal.as_dict()}, 200
    else:
        return {"details": "Invalid data"}, 404

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    return {"details":f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    if "task_ids" in request_body and type(request_body["task_ids"] == list):
        goal.tasks = [validate_model(Task, task_id) for task_id in request_body["task_ids"]]
        db.session.commit()
        return {"id": goal.goal_id, "task_ids": request_body["task_ids"]}
    else:
        return {"details": "Missing or invalid data for task_ids (must be a list)"}