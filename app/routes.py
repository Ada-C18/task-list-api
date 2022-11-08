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

    return_task_1 = {}
    def is_complete():
        if not request_body["completed_at"]:
            return False
        else:
            return True
    
    return_task_1 = {"task": {
            "id": task_1.id,
            "title":task_1.title,
            "description":task_1.description,
            "is_complete": is_complete()}}
    
    return make_response(jsonify(return_task_1), 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks(): 
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()   
    # tasks =Task.query.all()
    
    def is_complete():
        if "completed_at" in tasks_response == None:
            return True
        else:
            return False
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete()
        })
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
    task_dict = {}
    def is_complete():
        if "completed_at" in task_dict == None:
            return True
        else:
            return False
    task_dict={"task":
    {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete()
    }
}
    return jsonify(task_dict)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_id(Task, task_id)
    request_body = request.get_json()
    if "completed_at" not in request_body:
        request_body["completed_at"] = None

    task.title = title=request_body["title"],
    task.description=request_body["description"],
    task.completed_at=request_body["completed_at"]
    
    db.session.commit()

    def is_complete():
        if not request_body["completed_at"]:
            return False
        else:
            return True
    updated_task1 = {"task": {
            "id": task.id,
            "title":task.title,
            "description":task.description,
            "is_complete": is_complete()}}
    return make_response(jsonify(updated_task1), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def deleted_task(task_id):
    task = validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.id} "{task.title}" successfully deleted'}

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











