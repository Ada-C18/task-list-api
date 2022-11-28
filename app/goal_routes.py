from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.goal import Goal
from app.routes_helpers import validate_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"}), 400
    else: 
        new_goal = Goal(title=request_body["title"])
        db.session.add(new_goal)
        db.session.commit()

        return {"goal": new_goal.to_dict()}, 201

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"})

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_id_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    tasks = [validate_model(Task, task_id) for task_id in task_ids]

    for task in tasks:
        task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids,
    }

from app.models.task import Task

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        if task.goal_id == goal.id:
            tasks_response.append(task.to_dict())

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
        }
