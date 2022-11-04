from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# helper function
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task id: {task_id} must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))

    matching_task = Task.query.get(task_id)

    if not matching_task:
        abort(make_response(jsonify({"message": f"The {task_id} is not found"}), 404))

    return matching_task


# Create a Task: Valid Task With null completed_at
@task_bp.route("", methods=["POST"])
def create_task():
    response_body = request.get_json()

    if "title" not in response_body or\
       "description" not in response_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title = response_body["title"],
        description = response_body["description"]
    )
       
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.return_body()}),201


# Get Tasks: Getting Saved Tasks
@task_bp.route("", methods=["GET"])
def read_task():
    # title_param = request.args.get("title")
    # if title_param is not None:
    #     tasks = Task.query.filter_by(title=title_param)
    # else:
    tasks = Task.query.all()
    
    read_task_result = []
    for task in tasks:
        read_task_result.append(task.return_body())

    return jsonify(read_task_result), 200


# Get One Task: One Saved Task
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    chosen_task = validate_task(task_id)

    return jsonify({"task":chosen_task.return_body()}), 200


# Update Task
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = validate_task(task_id)
    request_body = request.get_json()

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    
    db.session.commit()
    return jsonify({"task":chosen_task.return_body()}), 200


# Deleting a Task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete = validate_task(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({"details": f'Task {task_to_delete.task_id} \
        "{task_to_delete.title}" successfully deleted'}), 200