from flask import Blueprint, jsonify, request, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at= None if "completed_at" not in request_body else request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False if new_task.completed_at == None else True
        }
    }

    response = make_response(jsonify(body), 201)
    return response


