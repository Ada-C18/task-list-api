from flask import Blueprint, jsonify, request
from app import db
from app.models.task import Task
from .routes_helper import validate_model
from datetime import datetime
import os
import requests
task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

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
        task_dict = Task.to_dict(task)
        response.append(task_dict)
    
    if sort_param == "asc":
        response = sorted(response, key=lambda task: task['title'])
    elif sort_param == "desc":
        response = sorted(response, key=lambda task: task['title'], reverse=True)

    return jsonify(response), 200



@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    selected_task = validate_model(Task, task_id)

    task_dict = Task.to_dict(selected_task)

    return jsonify({"task": task_dict}), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    selected_task = validate_model(Task, task_id)
    
    selected_task.completed_at = datetime.today()
    db.session.add(selected_task)
    db.session.commit()

    task_dict = Task.to_dict(selected_task)

    slack_path = "https://slack.com/api/chat.postMessage"
    SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
    }
    paramaters = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {selected_task.title}"
    }
    
    requests.get(url=slack_path, headers=headers, params=paramaters)

    return jsonify({"task": task_dict}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    selected_task = validate_model(Task, task_id)

    selected_task.completed_at = None

    db.session.add(selected_task)
    db.session.commit()

    task_dict = Task.to_dict(selected_task)

    return jsonify({"task": task_dict}), 200

@task_bp.route("<task_id>", methods=["PUT"])
def update_one_task(task_id):
    selected_task = validate_model(Task, task_id)
    
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
    selected_task = validate_model(Task, task_id)

    db.session.delete(selected_task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{selected_task.title}" successfully deleted'}), 200