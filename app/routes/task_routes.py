from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
# from sqlalchemy import asc, desc, select
import datetime
# from datetime import date
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

# def validate_request_body(body):
#     if "title" not in body or "description" not in body:
#         return {
#             "details": "Invalid data"
#         }, 400


def post_to_slack(task_title):
    URL = "https://slack.com/api/chat.postMessage"
    HEADER_AUTH = {"Authorization": os.environ.get("SL_TASK_BOT")}
    request_params = {
        "channel": "slack-bot-test-channel",
        "text": f"Someone just completed the task {task_title}"
    }

    response = requests.post(URL, params=request_params, headers=HEADER_AUTH)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    # request_body = validate_request_body(request_body)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = Task.query

    sort_query = request.args.get("sort")
    if sort_query == "desc":
        task_query = task_query.order_by(Task.title.desc())
    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.datetime.now()
    task_title = task.title

    db.session.commit()

    post_to_slack(task_title)

    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200
