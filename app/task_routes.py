from flask import Blueprint, request, make_response, jsonify, abort
from sqlalchemy import asc, desc
from app.models.task import Task
from app import db
from datetime import datetime
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def get_validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    order_by = request.args.get("sort")

    if order_by == 'asc':
        tasks = Task.query.order_by(asc('title')).all()
    elif order_by == 'desc':
        tasks = Task.query.order_by(desc('title')).all()
    else:
        tasks = Task.query.all()

    tasks_list = [task.to_dict() for task in tasks]
    return make_response(jsonify(tasks_list), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = get_validate_model(Task, task_id)
    current_task_response = {"task": task.to_dict()}

    return make_response(jsonify(current_task_response), 200)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)
    
    new_task = Task(title=request_body["title"],
                        description=request_body["description"])

    db.session.add(new_task) # track this object
    db.session.commit() # any changes that are pending commit those changes as data written in SQL
    current_task_response = {"task": new_task.to_dict()}
    return make_response(jsonify(current_task_response), 201)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = get_validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    current_task_response = {"task": task.to_dict()}
    return make_response(jsonify(current_task_response), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = get_validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_incompleted_task_to_complete(task_id):
    task = get_validate_model(Task, task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    slack_bot(task)
    current_task_response = {"task": task.to_dict()}
    return make_response(jsonify(current_task_response), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_completed_task_to_incomplete(task_id):
    task = get_validate_model(Task, task_id)
    task.completed_at = None

    db.session.commit()

    current_task_response = {"task": task.to_dict()}
    return make_response(jsonify(current_task_response), 200)


def slack_bot(task):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API")

    bot_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(PATH, data=bot_params, headers={"Authorization": SLACK_API_KEY})

