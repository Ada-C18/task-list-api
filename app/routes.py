from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from sqlalchemy import text
from app import db
import os
import requests
from datetime import datetime

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        if model_id:
            abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} is not found"}, 404))
    
    return model

@task_bp.route("", methods=["POST"])
def create_tasks():
    
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
            abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task(description=request_body["description"],
        title=request_body["title"]
        )

    db.session.add(new_task)
    db.session.commit()
    
    return make_response({"task": new_task.to_dict()},201)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return make_response({"task": task.to_dict()})

@task_bp.route("", methods=["GET"])
def get_tasks():
    
    sort_query = request.args.get("sort")
    title_query = request.args.get("title")
    task_query = Task.query

    if title_query:
        task_query = task_query.filter_by(title=title_query)
    
    if sort_query:
        if "asc" in sort_query:
            task_query = task_query.order_by(text('title asc'))
        elif "desc" in sort_query:
            task_query = task_query.order_by(text('title desc'))
        else:
            task_query = task_query.order_by(Task.id)

    tasks = task_query.all()

    task_list = [task.to_dict() for task in tasks]
    
    return jsonify(task_list)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()})

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})

def post_message_to_slack(message):
    
    path = "https://slack.com/api/chat.postMessage"
    data = {
        "channel": 'C049L1ZUVQV',
        "text": message, 
    }
    header_key = os.environ.get("authorization")

    response = requests.post(
        url=path, data=data,
        headers={"Authorization": header_key})

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task_id = validate_model(Task, task_id)

    task_id.completed_at = datetime.utcnow()

    post_message_to_slack(f"{task_id.title} was completed")

    db.session.commit()

    return make_response({"task": task_id.to_dict()})

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task_id = validate_model(Task, task_id)

    task_id.completed_at = None

    db.session.commit()

    return make_response({"task": task_id.to_dict()})







    
        
