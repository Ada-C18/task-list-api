import os
import requests
from app import db
from app.models.task import Task
from datetime import datetime
from dotenv import load_dotenv
from flask import Blueprint, request, make_response, jsonify, abort

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

def call_slack_bot(message):
    URL = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("TOKEN")
    query_params ={
        "channel" : "task-notifications",
        "text": message
        }
    header = {"Authorization" :f"Bearer {API_KEY}"}

    requests.post(URL, data=query_params, headers=header)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.order_by(Task.title).all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
        
    return jsonify(tasks_response)

@tasks_bp.route("/<model_id>", methods=["GET"])
def read_one_task(model_id):
    task = validate_model(Task, model_id)
    if not task.goal_id:
        return {"task":task.to_dict()}
    else:
        return {"task": {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}, 200

@tasks_bp.route("/<model_id>", methods=["PUT"])
def update_task(model_id):
    task = validate_model(Task, model_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}, 200

@tasks_bp.route("/<model_id>", methods=["DELETE"])
def delete_task(model_id):
    task = validate_model(Task, model_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}

@tasks_bp.route("/<model_id>/mark_complete", methods=["PATCH"])
def mark_complete(model_id):
    task = validate_model(Task, model_id)

    task.completed_at = datetime.now()

    db.session.commit()

    call_slack_bot(f"Someone just completed the task {task.title}")

    return {"task":task.to_dict()}, 200

@tasks_bp.route("/<model_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(model_id):
    task = validate_model(Task, model_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200