from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed at"]
        )
    db.session.add(new_task)
    db.session.commit()
    return make_response(f"Task '{new_task.title}' has been successfully created", 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    completed_at_query = request.args.get("completed at")
    task_query = Task.query
    if title_query:
        task_query = Task.query.filter_by(title=title_query)
    if completed_at_query:
        task_query = Task.query.filter_by(completed_at=completed_at_query)

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def task_endpoint(task_id):
    task = validate_task(task_id)

    return jsonify(task.to_dict())

@tasks_bp.route("/<task_id>", methods=["PUT"])
def task_update(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed at"]

    db.session.commit()
    return make_response(f"Task '{task.title}' has been updated successfully", 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def task_delete(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task '{task.title}' has been successfully deleted", 200)


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)
    
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task