from os import abort
import os
from app import db
from app.models.task import Task
from app.models.goal import Goal 
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from requests import post
from datetime import datetime, timezone
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(class_obj, object_id):
    try:
        object_id = int(object_id)
    except:
        abort(make_response(jsonify({"message": f"Task {object_id} has an invalid task_id"}), 400))

    query_result = class_obj.query.get(object_id)

    if not query_result:
        abort(make_response({"message": f"Task {object_id} not found"}, 404))

    return query_result

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        tasks_response = sorted(tasks_response, key=lambda dict: dict["title"])
    elif sorting_query == "desc":
        tasks_response = sorted(tasks_response, key=lambda dict: dict["title"], reverse=True) 

    return jsonify(tasks_response), 200
    
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    print(request_body)
    if "title" in request_body and "description" in request_body:
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        response_one_task = {"task": Task.to_dict(new_task)}
        return jsonify(response_one_task), 201
    else:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    response_one_task = {"task": Task.to_dict(task)}
    return jsonify(response_one_task), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update(request_body)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_updated_task = {"task": Task.to_dict(task)}
    return jsonify(response_updated_task), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.id} \"{task.title}\" successfully deleted"})

@tasks_bp.route("/<task_id>/<completion>", methods=["PATCH"])
def mark_task_completed(task_id, completion):
    task = validate_model(Task, task_id)

    if completion == "mark_complete":
        task.completed_at = datetime.now(timezone.utc)
        task.is_complete = True
        send_message_to_slack(task)

    elif completion == "mark_incomplete":
        task.completed_at = None
        task.is_complete = False

    db.session.commit()
    response_updated_task = {"task": Task.to_dict(task)}
    return jsonify(response_updated_task), 200

def send_message_to_slack(completed_task):
    channel_id = "C04AL1N1AFJ"
    SLACK_API_KEY = os.environ.get('API_KEY')
    PATH = "https://slack.com/api/chat.postMessage"
    slack_message_params = {
            "channel": channel_id, 
            "text": f"Someone just completed the task {completed_task.title}"}

    requests.post(PATH,
                data=slack_message_params,
                headers={"Authorization": SLACK_API_KEY}  
    )

