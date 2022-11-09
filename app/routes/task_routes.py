from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from datetime import datetime
import requests
import os

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

# validate 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not a valid id"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

# read all tasks
@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

# read one task
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    # return task.to_dict_one()
    return {"task": task.to_dict()}

# create new task
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
    except:
        return abort(make_response({"details": 'Invalid data'}, 400))

    db.session.add(new_task)
    db.session.commit()

    # return new_task.to_dict_one(), 201
    return {"task": new_task.to_dict()}, 201

# update task
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    # return task.to_dict_one()
    return {"task": task.to_dict()}

# delete task
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200)

# slack bot helper
def post_slack(task):
    url = 'https://slack.com/api/chat.postMessage'
    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    slack_key = os.environ.get("SLACK_KEY")
    headers = {
        "Authorization": f"Bearer {slack_key}"
    }

    requests.post(url, params=params, headers=headers)

# mark complete with patch
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    post_slack(task)

    # return task.to_dict_one()
    return {"task": task.to_dict()}

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    # return task.to_dict_one()
    return {"task": task.to_dict()}