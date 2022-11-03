from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: `{task_id}`. ID must be an integer."
        abort(make_response(jsonify({"message":response_str}), 400))

    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Bike with id `{task_id}` was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_task

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body or \
        "completed_at" not in request_body:
            return jsonify({"message": "Request body must contain title and description"}), 400

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"]
    )


    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.task_id}, 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    response = []
    for task in tasks:
        task_dict = {
           "id": task.task_id,
           "title": task.title,
           "description": task.description,
           "is_complete": task.completed_at
        }
        response.append(task_dict)
    return jsonify(response), 200

@task_bp.route("<task_id>", methods=["GET"])
def get_one_task(task_id):
    selected_task = get_one_task_or_abort(task_id)
    task_dict = {
        "id": selected_task.task_id,
        "title": selected_task.title,
        "description": selected_task.description,
        "is_complete": selected_task.completed_at
    }

    return jsonify(task_dict), 200

@task_bp.route("<task_id>", methods=["PUT"])
def update_one_task(task_id):
    selected_task = get_one_task_or_abort(task_id)
    
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"message": "Request must include title and description"}), 400

    selected_task.title = request_body["title"]
    selected_task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": selected_task.task_id}), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    selected_task = get_one_task_or_abort(task_id)

    db.session.delete(selected_task)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted task with id `{task_id}`"}), 200
