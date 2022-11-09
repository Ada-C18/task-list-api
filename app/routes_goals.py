from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request
from app.routes_tasks import Task

from app.route_helper import get_one_obj_or_abort

from app.slack_helper import sendSlackNotification

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal":
        {
            "id": new_goal.goal_id,
            "title": new_goal.title
        }
    }, 201


@goals_bp.route("", methods=["GET"])
def get_all_goal():

    goals = Goal.query.all()
    goals_response = [goal.to_dict()for goal in goals]
    return jsonify(goals_response), 200


@goals_bp.route("/<obj_id>", methods=["GET"])
def get_one_goal(obj_id):
    chosen_goal = get_one_obj_or_abort(Goal, obj_id)
    goal_dict = chosen_goal.to_dict()
    return jsonify({"goal": goal_dict}), 200


@goals_bp.route("/<obj_id>", methods=["PUT"])
def update_one_goal_new_value(obj_id):
    update_goal = get_one_obj_or_abort(Goal, obj_id)
    request_body = request.get_json()

    update_goal.title = request_body.get("title", update_goal.title)

    db.session.commit()
    return jsonify({"goal": update_goal.to_dict()}), 200


@goals_bp.route("/<obj_id>", methods=["DELETE"])
def delete_one_goal(obj_id):
    goal_to_delete = get_one_obj_or_abort(Goal, obj_id)

    db.session.delete(goal_to_delete)
    db.session.commit()
    return jsonify({"details": f'Goal {obj_id} "{goal_to_delete.title}" successfully deleted'})


@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_task_id_to_goal(goal_id):
    parent_goal = get_one_obj_or_abort(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body["task_ids"]

    for task_id in task_ids:
        task = get_one_obj_or_abort(Task, task_id)
        task.goal = parent_goal
        db.session.add(task)

    db.session.commit()

    return jsonify({"id": parent_goal.goal_id, "task_ids": task_ids})


@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_task_of_one_goal(goal_id):
    goal = get_one_obj_or_abort(Goal, goal_id)

    task_response = [task.to_dict() for task in goal.tasks]
    for task in task_response:
        task["goal_id"] = goal.goal_id
    return jsonify({"id": goal.goal_id, "title": goal.title, "tasks": task_response})
