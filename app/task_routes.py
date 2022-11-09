from flask import Blueprint
from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
import datetime as dt
import requests
from dotenv import load_dotenv
import os
load_dotenv()


tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#validate function 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


#CREATE a Task: Valid Task With null completed_at

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict_to_instance(request_body)

    except KeyError:
        abort(make_response({"details": "Invalid data"}, 400)) 

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.from_instance_to_dict()},201

# Get Tasks: Getting Saved Tasks
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else: 
        tasks = Task.query.order_by(Task.title.desc())

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.from_instance_to_dict())

    return jsonify(tasks_response)

# GET one task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task":task.from_instance_to_dict()}


# UPDATE Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.from_instance_to_dict()}


# Delete Task
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details":f'Task {task.task_id} "{task.title}" successfully deleted'}

# Helper Slack Bot 
def slack_bot(task):

    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    path = "https://slack.com/api/chat.postMessage"
    slack_channel = "task-notifications"
    task_text = f"Someone just completed the task {task.title}"

    query_params = {
    "channel": slack_channel,
    "text": task_text
    }
    requests.post(path, params=query_params, headers={"Authorization" : slack_token})

# PATCH method to update task
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def updated_incomplete_task_to_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = dt.date.today()

    db.session.commit()

    slack_bot_call = slack_bot(task)

    return {"task":task.from_instance_to_dict()}, 200

# PATCH Mark Incomplete on a Completed Task
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def updated_complete_task_to_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()
    return {"task":task.from_instance_to_dict()}, 200