from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if (("title") not in request_body
        or ("description") not in request_body):
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    task_response = Task.query.get(1)
    return make_response({"task": task_response.to_dict()}, 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()) #ColumnElement.desc() method produces a descending ORDER BY clause element
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()
    
    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task.id} \"{task.title}\" successfully deleted"}, 200)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_task(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.utcnow()
    db.session.commit()
    
    #send notif to Slack API
    params = {"channel": "task-notifications", "text": f"Someone just completed the task {task.title}"}
    header = {"Authorization": f"Bearer {os.environ.get('SLACKBOT_AUTH_TOKEN')}"}
    requests.post("https://slack.com/api/chat.postMessage", params=params, headers=header)
    
    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None
    db.session.commit()
    
    return make_response({"task": task.to_dict()}, 200)