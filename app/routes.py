from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        abort(make_response(jsonify({"details":"Invalid data"}), 400))
    
    else:
        if "completed_at" not in request_body:  
            new_incomplete_task = Task(
            title = request_body["title"],
            description = request_body["description"])

            db.session.add(new_incomplete_task)
            db.session.commit()
        
            new_incomplete_task_dict = {"id": new_incomplete_task.task_id,
            "title": new_incomplete_task.title,
            "description": new_incomplete_task.description,
            "is_complete": False}

        task_dict = {"task": new_incomplete_task_dict}

        return jsonify(task_dict), 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    response = []
    for task in tasks:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description}
        if not task.completed_at:
            task_dict["is_complete"] = False
        else:
            task_dict["completed_at"] = task.completed_at
        response.append(task_dict)
    
    return jsonify(response), 200

def validate_id(task_id):
    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Could not find task with id {task_id}"
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_task


@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    selected_task = validate_id(task_id)

    task_dict =  {"id": selected_task.task_id,
        "title": selected_task.title,
        "description": selected_task.description}
    
    if not selected_task.completed_at:
        task_dict["is_complete"] = False
    else:
        task_dict["completed_at"] = selected_task.completed_at
    
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
    
    task_dict =  {"id": selected_task.task_id,
        "title": selected_task.title,
        "description": selected_task.description}
    
    if not selected_task.completed_at:
        task_dict["is_complete"] = False
    else:
        task_dict["completed_at"] = selected_task.completed_at
    
    response_dict = {"task": task_dict}

    return response_dict, 200

@task_bp.route("/<task_id>", methods = ["DELETE"])
def delete_one_task(task_id):
    selected_task = validate_id(task_id)
    db.session.delete(selected_task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{selected_task.title}" successfully deleted'}), 200