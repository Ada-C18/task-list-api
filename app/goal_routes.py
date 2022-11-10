from app import db
from app.models.goal import Goal
from app.task_routes import get_task_from_id
from flask import abort, Blueprint, jsonify, make_response, request
import os

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"msg":f"Task {goal_id} not found"}, 404))

    return goal

def get_goal_from_id(goal_id):
    chosen_goal = Goal.query.get(goal_id)
    if chosen_goal is None:
        return abort(make_response({"msg": f"Could not find goal item with id: {goal_id}"}, 404))
    return chosen_goal

@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal=Goal(
            title=request_body["title"]
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.to_dict()}), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    result = [goal.to_dict() for goal in goals]
    return jsonify(result), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    chosen_goal = get_goal_from_id(goal_id)
    return jsonify({"goal":chosen_goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body=request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal":goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    goal_title = goal.title

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal_title}" successfully deleted'}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_ids_to_goal(goal_id):
    goal = get_goal_from_id(goal_id)

    request_body = request.get_json()

    # new_tasks=Goal(
    #     tasks=request_body["tasks"]
    # )
    new_tasks = request_body["task_ids"]

    task_ids = []
    for task in new_tasks:
        task=get_task_from_id(task)
        # goal.tasks.append(task)
        task.goal_id = goal.goal_id
        task_ids.append(task.task_id)
   
    db.session.commit()

    return jsonify({"id": goal.goal_id, "task_ids": task_ids}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_specific_goal(goal_id):
    goal = get_goal_from_id(goal_id)

    result = goal.to_dict_relationship()

    return jsonify(result), 200
# chosen_goal = get_goal_from_id(goal_id)