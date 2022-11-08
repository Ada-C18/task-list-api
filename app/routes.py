
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request

from app.route_helper import get_one_obj_or_abort
from datetime import datetime

from app.slack_helper import sendSlackNotification

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return {
        "task":
        {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": new_task.completed_at is not None
        }
    }, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_filter = request.args.get("sort")
    if sort_filter == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_filter == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@tasks_bp.route("/<obj_id>", methods=["GET"])
def get_one_task(obj_id):
    chosen_task = get_one_obj_or_abort(Task, obj_id)
    task_dict = chosen_task.to_dict()
    return jsonify({"task": task_dict}), 200


@tasks_bp.route("/<obj_id>", methods=["PUT"])
def update_task_with_new_value(obj_id):

    update_task = get_one_obj_or_abort(Task, obj_id)
    request_body = request.get_json()

    update_task.title = request_body.get("title", update_task.title)
    update_task.description = request_body.get(
        "description", update_task.description)
    update_task.completed_at = request_body.get(
        "completed_at", update_task.completed_at)

    db.session.commit()
    return jsonify({"task": update_task.to_dict()}), 200


@tasks_bp.route("/<obj_id>", methods=["DELETE"])
def delete_one_task(obj_id):
    task_to_delete = get_one_obj_or_abort(Task, obj_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f'Task {obj_id} "{task_to_delete.title}" successfully deleted'})


@tasks_bp.route("/<obj_id>/mark_complete", methods=["PATCH"])
def complete_task(obj_id):

    update_task = get_one_obj_or_abort(Task, obj_id)
    update_task.completed_at = datetime.utcnow()

    db.session.commit()
    sendSlackNotification(update_task.title)
    return jsonify({"task": update_task.to_dict()}), 200


@tasks_bp.route("/<obj_id>/mark_incomplete", methods=["PATCH"])
def uncomplete_task(obj_id):

    update_task = get_one_obj_or_abort(Task, obj_id)
    update_task.completed_at = None

    db.session.commit()
    return jsonify({"task": update_task.to_dict()}), 200


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
    update_goal = get_one_obj_or_abort(Goal,obj_id)
    request_body = request.get_json()

    update_goal.title = request_body.get("title", update_goal.title)

    db.session.commit()
    return jsonify({"task": update_goal.to_dict()}), 200

@goals_bp.route("/<obj_id>", methods=["DELETE"])
def delete_one_goal(obj_id):
    goal_to_delete = get_one_obj_or_abort(Goal,obj_id)

    db.session.delete(goal_to_delete)
    db.session.commit()
    return jsonify({"details": f'Task {obj_id} "{goal_to_delete.title}" successfully deleted'})