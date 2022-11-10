import os
from app import db
from app.models.goal import Goal
from app.models.task import Task
from .tasks import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def check_for_missing_data(request_body):
    if "title" not in request_body:
            return False
    return True

@bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if not check_for_missing_data(request_body):
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal": new_goal.to_dict()}, 201)

@bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    all_goals = [goal.to_dict() for goal in goals]

    return jsonify(all_goals)

@bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    one_goal = validate_model(Goal, goal_id)
    return make_response({"goal": one_goal.to_dict()}, 200)

@bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal": goal.to_dict()}, 200)

@bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200)

@bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids = request_body["task_ids"]
    for task_id in task_ids:
        curr_task = validate_model(Task, task_id)
        curr_task.goal = goal

    db.session.commit()

    return make_response({"id": goal.goal_id, "task_ids": task_ids}, 200)