from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def get_one_task_or_error(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_body = "Invalid data"
        abort(make_response(jsonify({"details": response_body}), 400))

    task_found = Task.query.get(task_id)

    if task_found is None:
        response_body = "Task id not found"
        abort(make_response(jsonify({"details": response_body}), 404))

    return task_found

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("", methods=["POST"])
def add_task():

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response = Task.to_dict(new_task)

    return jsonify({"task": response}), 201 

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    sort_params = request.args.get("sort")

    tasks = Task.query.all()

    response = []

    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
        response.append(task_dict)

    if sort_params == "asc":
        response = sorted(response, key=lambda task: task['title'])
        #give client list of titles in ascending order by alphabet 
    elif sort_params == "desc":
        response = sorted(response, key=lambda task: task['title'], reverse=True)
        #give client list of titles in descending order by alphabet, reverse=True
    return jsonify(response), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_task_or_error(task_id)

    response = Task.to_dict(chosen_task)

    return jsonify({"task": response}), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_title_and_description(task_id):
    task_to_update = get_one_task_or_error(task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    response_body = Task.to_dict(task_to_update)

    return jsonify({"task": response_body}), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_data_from_db(task_id):

    task_to_delete = get_one_task_or_error(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    response_body = f'Task {task_id} "{task_to_delete.title}" successfully deleted'
    return jsonify({"details": response_body}), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task_to_complete = get_one_task_or_error(task_id) # 1, whatever title, description and complete?

    task_to_complete.completed_at = datetime.today()
    
    db.session.add(task_to_complete)
    db.session.commit()
    
    return jsonify({"task": task_to_complete.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    incomplete_task = get_one_task_or_error(task_id)

    incomplete_task.completed_at = None

    db.session.add(incomplete_task)
    db.session.commit()

    return jsonify({"task": incomplete_task.to_dict()}), 200
