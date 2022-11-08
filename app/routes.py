from flask import Blueprint, jsonify, abort, request, make_response
from app import db
from app.models.task import Task
from sqlalchemy import desc , asc
import datetime
import os
import requests

# ----- TASK ROUTE FUNCTIONS ----------

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():

    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"
    }, 400)
    
    if "completed_at" not in request_body:
        request_body["completed_at"] = None

    new_task = Task(
                    title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_list = []
    
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query =="desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:   
        tasks = Task.query.all()

    for task in tasks:
        task_list.append(task.to_dict())
    
    return jsonify(task_list)


def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response({"message":f"{cls.__name__} {id} invalid"}, 400))

    obj = cls.query.get(id)

    if not obj:
        abort(make_response({"message":f"{cls.__name__}{id} not found"}, 404))

    return obj
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_id(Task, task_id)

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)
    if "completed_at" not in request_body:
        request_body["completed_at"] = None

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    delete_response = {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}

    return make_response(jsonify(delete_response), 200)

def slack_bot_message(message):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get('API_KEY')


    query_params = {
        "channel": "task-notifications",
        "text": message
    }

    requests.post(PATH, data=query_params, headers={"Authorization": f"Bearer {SLACK_API_KEY}"})


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])

def update_incomplete_task(task_id):

    task = validate_id(Task, task_id)
    
    task.completed_at = datetime.datetime.utcnow()

    db.session.commit()

    def is_complete():
        return True
    
    slack_bot_message(f"Someone just completed the task {task.title}")

    return make_response(jsonify({"task": task.to_dict()}), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])

def update_complete_task(task_id):

    task = validate_id(Task, task_id)

    task.completed_at =  None

    db.session.commit()

    def is_complete():
        return False


    return make_response(jsonify({"task": task.to_dict()}), 200)
