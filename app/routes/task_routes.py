from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
from app import os
from .validate_model import validate_model

SLACK_TOKEN = os.environ.get('SLACK_TOKEN', None)

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

"""Wave 1"""

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "task": new_task.to_dict()
    }), 201

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    sort_request = request.args.get("sort")
    # task_list = []


    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())

    """WAVE 2"""
    
    if sort_request == "asc":
        task_response = sorted(task_response, key=lambda a: a["title"])
    elif sort_request == "desc":
        task_response = sorted(task_response, key=lambda d: d["title"], reverse=True) 

    return jsonify(task_response)

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
  
    return make_response(jsonify({"task":task.to_dict()}))

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    task_dict = {
    "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }

    db.session.delete(task)
    db.session.commit()

    return jsonify(task_dict), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    response_body = {"task": task.to_dict()}
    db.session.commit()
    return jsonify(response_body), 200
 
"""WAVE 3"""

# @task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
# def mark_task_complete(task_id):
#     task = validate_model(Task, task_id)
#     task.completed_at = datetime.now()
#     db.session.commit()
#     return jsonify(task=task.to_dict()), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify(task=task.to_dict()), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_completed_task_and_incomplete_task(task_id):
    task = validate_model(Task, task_id)
    if task:
        task.completed_at = datetime.now()
        db.session.commit()
    
    db.session.commit()
    
    return jsonify(task=task.to_dict()), 200
