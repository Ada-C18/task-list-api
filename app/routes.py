import datetime
import os
from flask import Blueprint, request, make_response, abort, jsonify
from app.models.task import Task
from app.models.goal import Goal
from app import db
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

# HELPER FUNCTION
def validate_id(class_obj, id):
    try:
        object_id = int(id)
    except:
        abort(make_response({"details": f"{class_obj} {id} is invalid"}, 400))

    query_result = class_obj.query.get(object_id)
    if not query_result:
        abort(make_response({"details": f"{class_obj} {id} is not found"}, 404))
    
    return query_result

def send_slack_message(message):
    path = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("API_KEY")
    query_params = {
        "channel": "happychannel",
        "text": message
    }
    query_header = {"Authorization": f"Bearer {API_KEY}"}
    return requests.post(path, params = query_params, headers = query_header)



# CREATE RESOURCE
@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body= request.get_json()

    try:
        new_task = Task.from_json(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.to_dict(), 201)


# GET ALL RESOURCE
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks_response = []
    sort_param = request.args.get("sort")
    tasks = None

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append(task.to_dict()["task"])

    return jsonify(tasks_response), 200


# GET ONE RESOURCE
@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_id(Task, task_id)

    return jsonify(task.to_dict()), 200


# UPDATE RESOURCE
@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()

    return make_response(task.to_dict())

# DELETE RESOURCE
@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})


# UPDATE COMPLETE STATUS
@tasks_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    task = validate_id(Task, task_id)

    task.completed_at = datetime.datetime.utcnow()

    db.session.commit()
    send_slack_message(f"Someone just completed the task {task.title}")
    return make_response({"task":
                                {
                                    "id": task.task_id,
                                    "title": task.title,
                                    "description": task.description,
                                    "is_complete": True
                                }}, 200)

 

@tasks_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response({"task":
                                {
                                    "id": task.task_id,
                                    "title": task.title,
                                    "description": task.description,
                                    "is_complete": False
                                }}, 200)
