from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# def get_one_task(task_id):
    
#     matching_task = Task.query.get(task_id)

#     return matching_task

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    response = new_task

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(response), 201 # is this giving me the output needed?

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False # will need help figuring out how to use this
        }
        response.append(task_dict)
    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    task = Task.query.get(task_id)

    return {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False
    }, 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    task = Task.query.get(task_id)

    request_body = request.get_json()
    response = task

    