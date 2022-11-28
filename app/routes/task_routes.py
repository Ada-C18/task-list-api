from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime
from app import os
from .validate_model import validate_model
import os
import requests

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
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if sort_query == "asc": 
                tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    elif title_query:
            tasks = Task.query.get(title=title_query)
    else:
            tasks = Task.query.all()

    task_list = [task.to_dict() for task in tasks]

    return make_response(jsonify(task_list), 200)


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
 
"""WAVE 3 & 4"""
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
SLACK_URL = os.environ.get('SLACK_URL')

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return jsonify(task=task.to_dict()), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_completed_task_and_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    post_message(task)

    db.session.commit()
    return jsonify(task=task.to_dict()), 200

def post_message(task):
        KEY = os.environ.get("SLACK_TOKEN")
        PATH = SLACK_URL#"https://slack.com/api/chat.postMessage"
        HEADER = {"Authorization": KEY}
        PARAMS = {"channel": "task-completed","text": f"Someone just completed the task {task}."}
        requests.post(url=PATH, data=PARAMS, headers=HEADER)