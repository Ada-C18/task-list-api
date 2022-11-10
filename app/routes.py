from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import desc, asc
from datetime import date
import requests
# import slack
import os
from pathlib import Path
from dotenv import load_dotenv

# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)
# client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
load_dotenv()
slack_token = os.environ.get('SLACK_TOKEN')


def post_to_slack(text, blocks=None):
    return requests.post('https://slack.com/api/chat.postMessage',
                         {'token': slack_token, 'channel': '#slack-bot-test-channel', 'text': text})


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task


@ tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    if "completed_at" not in request_body:
        request_body["completed_at"] = None

    new_task = Task(title=request_body['title'],
                    description=request_body['description'],
                    completed_at=request_body['completed_at'])

    db.session.add(new_task)
    db.session.commit()

    return make_response({'task': new_task.to_dict()}, 201)


@ tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    sort_query = request.args.get("sort")
    if sort_query == 'desc':
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_query == 'asc':
        tasks = Task.query.order_by(Task.title.asc())

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)


@ tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    if not task.goal_id:
        return {'task': task.to_dict()}
    else:
        task_dict = task.to_dict()
        # task_as_dict["goal_id"] = self.goal_id
        task_dict["goal_id"] = task.goal_id

        return {'task': task_dict}


@ tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({'task': task.to_dict()}, 200)

# wave 3 PATCH


@ tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.completed_at = date.today()

    text = f"Someone just completed the task {task.title}"
    post_to_slack(text)

    db.session.commit()
    # client.chat_postMessage(
    #     channel='#slack-bot-test-channel', text=f"Someone just completed the task {task.title}")

    return make_response({'task': task.to_dict()}, 200)


@ tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None

    db.session.commit()

    return make_response({'task': task.to_dict()}, 200)


@ tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    return make_response({f"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)
