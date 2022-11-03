from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details":"Invalid data"}, 400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }, 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    all_tasks = Task.query.all()
    response_body = []
    
    for task in all_tasks:
        response_body.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False if task.completed_at is None else True
            }
        )
    return jsonify(response_body)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task():
    pass

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task():
    pass

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task():
    pass