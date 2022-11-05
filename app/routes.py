from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from datetime import datetime

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: `{task_id}`. ID must be an integer."
        abort(make_response(jsonify({"message":response_str}), 400))

    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Task with id `{task_id}` was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_task

def get_completed_task(task):
    if task.completed_at is None:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    else:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "completed_at": task.completed_at
        }
    return task_dict

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    task_dict = Task.to_dict(new_task)

    return jsonify({"task": task_dict}), 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    
    tasks = Task.query.all()

    response = []
    for task in tasks:
        task_dict = get_completed_task(task)
        response.append(task_dict)
    
    if sort_param == "asc":
        response = sorted(response, key=lambda task: task['title'])
    elif sort_param == "desc":
        response = sorted(response, key=lambda task: task['title'], reverse=True)

    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    selected_task = get_one_task_or_abort(task_id)

    task_dict = Task.to_dict(selected_task)

    return jsonify({"task": task_dict}), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    selected_task = get_one_task_or_abort(task_id)
    
    selected_task.completed_at = datetime.today()

    db.session.add(selected_task)
    db.session.commit()

    task_dict = Task.to_dict(selected_task)


    return jsonify({"task": task_dict}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    selected_task = get_one_task_or_abort(task_id)

    selected_task.completed_at = None

    db.session.add(selected_task)
    db.session.commit()

    task_dict = Task.to_dict(selected_task)

    return jsonify({"task": task_dict}), 200

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
    
    task_dict = Task.to_dict(selected_task)
    return jsonify({"task": task_dict}), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    selected_task = get_one_task_or_abort(task_id)

    db.session.delete(selected_task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{selected_task.title}" successfully deleted'}), 200
