from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

# helper function to structure request response json
def make_task_dict(task):
        task_dict = {"id": task.task_id,
        "title": task.title,
        "description": task.description}

        if task.completed_at is None:
            task_dict["is_complete"] = False
        else:
            task_dict["is_complete"] = True
            task_dict["completed_at"] = task.completed_at
        
        return task_dict

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        abort(make_response(jsonify({"details":"Invalid data"}), 400))
    
    else:
        new_task = Task(
        title = request_body["title"],
        description = request_body["description"])

        if "completed_at" in request_body:
            new_task.completed_at = request_body["completed_at"]

        db.session.add(new_task)
        db.session.commit()

        new_task_dict = {"task": make_task_dict(new_task)}
        return jsonify(new_task_dict), 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    response = []
    for task in tasks:
        task_dict = make_task_dict(task)
        response.append(task_dict)
    
    return jsonify(response), 200

#helper function to validate that task ids are valid
def validate_id(task_id):
    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Could not find task with id {task_id}"
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_task


@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    selected_task = validate_id(task_id)
    task_dict = make_task_dict(selected_task)
    response_dict = {"task": task_dict}
    return response_dict, 200


@task_bp.route("/<task_id>", methods = ["PUT"])
def update_task_with_new_vals(task_id):
    selected_task = validate_id(task_id)

    request_body = request.get_json()
    if "title" in request_body:
        selected_task.title = request_body["title"]
    if "description" in request_body:
        selected_task.description = request_body["description"]
    
    db.session.commit()
    
    task_dict = make_task_dict(selected_task)
    response_dict = {"task": task_dict}
    return response_dict, 200

@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    selected_task = validate_id(task_id)
    db.session.delete(selected_task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{selected_task.title}" successfully deleted'}), 200