from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from datetime import date
import requests
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if request_body.get("title") and request_body.get("description"):
        new_task = Task.from_dict(request_body)
    else:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()
    
    response_dict = {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": False
    }
    return jsonify({"task": response_dict}), 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    sort_query_value = request.args.get("sort")
    tasks_response.sort(
        key=lambda task: task["title"], reverse=sort_query_value == "desc")
    
    return jsonify(tasks_response)

def validate_task(task_id):
    task = Task.query.get(task_id)
   
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))
    
    return task

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    chosen_task = validate_task(task_id)
    return jsonify({"task": chosen_task.to_dict()})

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = validate_task(task_id)
    request_body = request.get_json()

    try:
        chosen_task.title = request_body["title"]
        chosen_task.description = request_body["description"]
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    
    db.session.commit()
    
    return jsonify({"task": chosen_task.to_dict()})

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    chosen_task = validate_task(task_id)
    
    db.session.delete(chosen_task)
    db.session.commit()

    return jsonify({"details": f"Task {chosen_task.task_id} \"Go on my daily walk 🏞\" successfully deleted"})

def call_slack_api(text):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": os.environ.get("SLACK_TOKEN")}
    query_params = {
        "channel": "task-notifications",
        "text": text
        }

    response = requests.post(url, headers=headers, params=query_params)
    return response


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    chosen_task = validate_task(task_id)
    chosen_task.completed_at = date.today()
    call_slack_api(f"Someone just completed the task {chosen_task.title}")

    db.session.commit()

    chosen_task_dict = chosen_task.to_dict()
    chosen_task_dict["is_complete"] = True
    return jsonify({"task": chosen_task_dict})


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    chosen_task = validate_task(task_id)
    chosen_task.completed_at = None

    db.session.commit()

    return jsonify({"task": chosen_task.to_dict()})




