
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request

from app.route_helper import get_one_obj_or_abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

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
    task_query = request.args.get("title")
    if task_query:
        tasks = request.args.filter_by(title=task_query)
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@tasks_bp.route("/<obj_id>", methods=["GET"])
def get_one_task(obj_id):
    chosen_task = get_one_obj_or_abort(Task, obj_id)
    task_dict = chosen_task.to_dict()
    return jsonify(task_dict), 200


# @tasks_bp.route("", methods=["PUT"])
# def update_task_with_new_value(task_id)
