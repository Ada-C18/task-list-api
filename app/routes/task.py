from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import date
import requests
import os

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

SLACK_PM_URL = "https://slack.com/api/chat.postMessage"
CHANNEL_ID = "C049V84LRHD"

def send_completed_message(task):
    try:
        MESSAGE = f"Someone just completed the task {task.title}"
        AUTH_HEADER = {"Authorization": f"Bearer {os.environ.get('SLACK_KEY')}"}

        parameters = {
            "channel": CHANNEL_ID,
            "text": MESSAGE
        }

        response = requests.post(SLACK_PM_URL, params=parameters,
                    headers=AUTH_HEADER)
        response_body = response.json()
        
        if response_body["ok"] == True:
            print("Task completion message successfully posted to Slack.")

    except requests.HttpError:
        print("Task completion message was unable to be posted to Slack.")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task


def validate_dict_title_desc(request_body):
    request_body = dict(request_body)
    if not (request_body.get("title", False) and request_body.get("description", False)):
        abort(make_response({"details": "Invalid data"}, 400))


@bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    sort_query = request.args.get("sort")

    task_query = Task.query

    if sort_query:
        task_query = task_query.order_by(Task.title.desc()) if sort_query == "desc" else task_query.order_by(Task.title.asc())

    tasks = task_query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)


@bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)
    task_response = {
        "task": task.to_dict()
    }
    return jsonify(task_response)


@bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    validate_dict_title_desc(request_body)
    new_task = Task.task_from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return make_response(jsonify(response_body), 201)


@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)

    request_body = request.get_json()
    validate_dict_title_desc(request_body)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_body = {"task": task.to_dict()}

    return jsonify(response_body)


@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)
    task_id = task.task_id
    task_title = f"\"{task.title}\""

    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f'Task {task_id} {task_title} successfully deleted'
    }

    return jsonify(response_body)


@bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_task_complete(id):
    task = validate_task(id)

    task.completed_at = date.today()
    task.is_complete = True

    db.session.commit()

    send_completed_message(task)
    response_body = {"task": task.to_dict()}

    return jsonify(response_body)

@bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(id):
    task = validate_task(id)

    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    response_body = {"task": task.to_dict()}

    return jsonify(response_body)
