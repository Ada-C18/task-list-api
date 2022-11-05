from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

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
        # or \
        # "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = None
    )

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
            }
        }

    return jsonify(response), 201 

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("", methods=["GET"])
def get_all_tasks():

    tasks = Task.query.all()

    response = []

    for task in tasks:
        if task is None:
            response_body = "Whoopsie daisy! Task id is lost and was not found"
            return jsonify(response_body), 404
        else:
            task_dict = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
            response.append(task_dict)
    return jsonify(response), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_task_or_error(task_id)

    response_dict = {
        "task": {
            "id": chosen_task.task_id,
            "title": chosen_task.title,
            "description": chosen_task.description,
            "is_complete": False
            }
        }
    return jsonify(response_dict), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task_title_and_description(task_id):
    task_to_update = get_one_task_or_error(task_id)

    request_body = request.get_json()

    task_to_update.title = request_body["title"]
    task_to_update.description = request_body["description"]

    db.session.commit()

    response_body = {       
        "task": {
            "id": task_to_update.task_id,
            "title": task_to_update.title,
            "description": task_to_update.description,
            "is_complete": False
            }
        }
    return jsonify(response_body), 200

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_data_from_db(task_id):

    task_to_delete = get_one_task_or_error(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    response_body = f'Task {task_id} "{task_to_delete.title}" successfully deleted'
    return jsonify({"details": response_body}), 200