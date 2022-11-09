from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import date
import os
from dotenv import load_dotenv
import requests
import json
load_dotenv()


task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')


# def validate_id(cls, id):
#     # invalid id type
#     try:
#         id = int(id)
#     except ValueError:
#         abort(make_response(jsonify({
#             "details": "Invalid data"
#         }), 400))

#     # id not found
#     model = cls.query.get(id)

#     if not model:
#         abort(make_response({"details": "Id not found"})), 404


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":
                          Task.to_dict(new_task)
                          }), 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():

    title_query = request.args.get("sort")

    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif title_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = [Task.to_dict(task)for task in tasks]

    return jsonify(tasks_response), 200


@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return make_response({"details": "Id not found"}), 404

    return make_response({"task":
                          Task.to_dict(task)
                          })


@task_bp.route("/<task_id>", methods=["PUT"])
def edit_task(task_id):
    # task = validate_id(Task, task_id)
    task = Task.query.get(task_id)

    if not task:
        return make_response({"details": "Id not found"}), 404
    request_body = request.get_json(task_id)

    task.update(request_body)

    db.session.commit()

    return make_response({"task":
                          Task.to_dict(task)
                          })


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return make_response({"details": "Id not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return make_response({f"details": f'Task {task_id} \"{task.title}\" successfully deleted'}), 200


def post_message_to_slack(param):
    task = Task.query.get(param)
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': os.environ.get("SLACK_TOKEN"),
        'channel': "C049FQLJTBN",
        'text': f"Someone just completed the task {task.title}"}).json()


@task_bp.route("/<task_id>/<complete>", methods=["PATCH"])
def patch_task_complete(task_id, complete):

    task = Task.query.get(task_id)

    if not task:
        return make_response({"details": "Id not found"}), 404

    if complete == "mark_complete":
        task.completed_at = date.today()
        post_message_to_slack(task_id)
        # client.chat_postMessage(channel='#slack-bot-test-channel',text=f"Someone just completed the task {task.title}")

    elif complete == "mark_incomplete":
        task.completed_at = None

    db.session.commit()

    return make_response({"task":
                          Task.to_dict(task)
                          })
