from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import date, datetime, timedelta
import requests
datetime.utcnow()
import os

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    if "completed_at" not in request_body:
        request_body["completed_at"] = None

    task_1 = Task(title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"])
    
    db.session.add(task_1)
    db.session.commit()
    
    return {"task":task_1.to_dict()}, 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks(): 
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()   

    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response)


def validate_id(cls, id):
    try:
        id = int(id)
    except:
        abort(make_response ({"Message": f"{cls.__name__} {id} invalid."}, 400))
    
    obj = cls.query.get(id)
    if not obj:
        abort(make_response({"Message": f"{cls.__name__} {id} not found."}, 404))
    return obj
        

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_id(Task, task_id)
    
    if task.goal_id is None:
        return {"task": task.to_dict()}, 200
    else:
        return {"task": task.from_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json()

    if "completed_at" not in request_body:
        request_body["completed_at"] = None

    task.title=request_body["title"],
    task.description=request_body["description"],
    task.completed_at=request_body["completed_at"]
    
    db.session.commit()
    
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def deleted_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}

def slack_bot(message):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

    query_params = {
        "channel": "task-notifications",
        "text": message
    }
    requests.post(PATH, data=query_params, headers={"Authorization": f"Bearer {SLACK_API_KEY}"})
    

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_as_completed(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.utcnow()
    
    slack_bot(f"Someone just completed the task {task.title}")
    
    db.session.commit()
    
    return {"task": task.to_dict()}, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_as_incomplete(task_id):
    task = validate_id(Task, task_id)    
    task.completed_at = None
    
    db.session.commit()
    
    return {"task": task.to_dict()}, 200











