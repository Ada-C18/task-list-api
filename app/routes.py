
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# def validate_task():
#     pass


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    is_complete = False
    if new_task.completed_at is not None:
        is_complete = True

    return {
        "task":
        {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": is_complete
        }
    }, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks_response = []

    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append({"id": task.task_id, "title": task.title,
                               "description": task.description, "is_complete": task.is_complete})

    return jsonify(tasks_response)
