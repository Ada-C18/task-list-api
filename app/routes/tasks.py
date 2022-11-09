from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime, datetime
import os
import requests
from app.routes.helper_functions import validate_model

bp = Blueprint("tasks", __name__, url_prefix = "/tasks")


@bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response(dict(task = task.to_dict()), 200)


@bp.route("", methods=["GET"])
def read_all_planets():

    sort_query = request.args.get('sort')

    tasks = Task.query

    if sort_query == 'asc':
        tasks = tasks.order_by(Task.title.asc())

    if sort_query == 'desc':
        tasks = tasks.order_by(Task.title.desc())

    tasks = tasks.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200

@bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        request_body["title"] and request_body["description"]
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    try:
        request_body["completed_at"]
    except:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    else:
        new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(dict( task = new_task.to_dict()), 201)

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    try:
        request_body["completed_at"]
    except:
        task.title = request_body["title"]
        task.description = request_body["description"]

    else:
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]

    db.session.commit()
    return make_response(dict(task = task.to_dict()), 200)

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()  
    return make_response({'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

def slack_bot(message):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("API_KEY")

    bot_params = {
        "channel" : "#task-notifications",
        "text" : message
    }

    bot_header = {
        "Authorization" : SLACK_API_KEY
    }

    requests.post(PATH, data=bot_params, headers=bot_header)

@bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_mark_complete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at == None or isinstance(task.completed_at, datetime):
        task.completed_at = datetime.now()
        db.session.commit()  

        slack_bot(f"Someone just completed the task {task.title}")

        return make_response(dict(task = dict(
            id=task.task_id,
            title=task.title,
            description=task.description,
            is_complete=True)), 200)

@bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at == None or isinstance(task.completed_at, datetime):
        task.completed_at = None
        db.session.commit()

        return make_response(dict(task = dict(
            id=task.task_id,
            title=task.title,
            description=task.description,
            is_complete=False)), 200)

