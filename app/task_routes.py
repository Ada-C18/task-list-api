from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
import requests
import os

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "title" not in request_body or "description" not in request_body:
        return make_response(jsonify({"details":"Invalid data"}), 400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task":new_task.to_dict()}),201) 
                       
@task_bp.route("", methods=["GET"])
def get_tasks():
    tasks_response = []
    tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]

    

    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks_response = sorted(tasks_response, key = lambda d: d["title"])
    elif sort_query == "desc":
        tasks_response = sorted(tasks_response, key = lambda d: d["title"], reverse=True)
    
    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response(jsonify({"task":task.to_dict()}),200) 

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify({"task":task.to_dict()}),200) 

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.utcnow()
    
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    data = {
        "channel":"task-notifications",
        "text":f"Someone just completed the task {task.title}"
    }

    headers = {"Authorization": f"Bearer {os.environ.get('AUTHORIZATION')}"}

    requests.post(url=url, data=data, headers=headers)
    
    return make_response(jsonify({"task":task.to_dict()}),200) 

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response(jsonify({"task":task.to_dict()}),200) 







