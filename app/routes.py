import datetime
import requests
import os
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, abort, request

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, id):
    try:
        model_id = int(id)
    except:
        abort(make_response({"message":f"{cls.__name__} {id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))

    return model

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.instance_from_json(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc())    #STOPPED HERE
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc())    #STOPPED HERE
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return {"task": task.to_dict()}

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}))

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.datetime.now()

    post_message_to_slack(task)

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))

def post_message_to_slack(a_task):
    token = os.environ.get("SLACKBOT_TOKEN")
    url = "https://slack.com/api/chat.postMessage"
    auth_header = {'Authorization': token}
    param_data = {"channel":"task-notifications",
                "text":f"Someone just completed the task {a_task.title}"}

    requests.post(url, headers = auth_header, data=param_data)