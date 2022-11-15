from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import datetime 
import requests
import os 

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    try:
        request_body = request.get_json()
        if "completed_at" not in request_body:
            request_body["completed_at"] = None

        new_task = Task.from_json(Task, request_body)
        db.session.add(new_task)
        db.session.commit()

        tasks_response = {}

        task_in_dict = new_task.to_dict()
        tasks_response["task"]=task_in_dict
        return jsonify (tasks_response), 201

    except:
        response_body = {}
        response_body["details"] = "Invalid data"
        return response_body, 400


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_query = request.args.get("completed_at")
    sort_query = request.args.get("sort")

    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif description_query:
        tasks = Task.query.filter_by(description=description_query)
    elif completed_query:
        tasks = Task.query.filter_by(completed_at=completed_query)
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify (tasks_response), 200

@tasks_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_model(Task, id)
    tasks_response = {}
    task_in_dict = task.to_dict()
    tasks_response["task"]=task_in_dict
    return jsonify (tasks_response), 200

@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    # not working 
    # task.completed_at = request_body["completed_at"]

    db.session.commit()

    tasks_response = {}
    task_in_dict = task.to_dict()
    tasks_response["task"]=task_in_dict

    return jsonify (tasks_response), 200

@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)

    db.session.delete(task)

    db.session.commit()
    response_body = {}
    response_body["details"] = (f'Task {id} "{task.title}" successfully deleted')

    return response_body, 200

@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incomplete_task(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.datetime.utcnow()
    db.session.commit()

    slack_bot(f"Someone just completed the task {task.title}")

    task_in_dict = task.to_dict()
    task_in_dict["is_complete"] = True
    tasks_response = {"task" : task_in_dict}

    return jsonify (tasks_response), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_on_complete_task(id):
    task = validate_model(Task, id)

    task.completed_at = None
    
    db.session.commit()

    tasks_response = {}
    task_in_dict = task.to_dict()
    tasks_response["task"]=task_in_dict

    return jsonify (tasks_response), 200

# slack bot helper func
def slack_bot(msg):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

    query_params = {
        "channel" : "#task-notifications",
        "text" : msg
    }
    headers = {
        "Authorization" : f"Bearer {SLACK_API_KEY}"
    }

    requests.post(PATH, params=query_params, headers=headers)
# verify id
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model