from app import db
from app.models.task import Task 
from app.models.goal import Goal 
from datetime import datetime
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc
import requests  
import os
from dotenv import load_dotenv
load_dotenv()

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} is invalid, please search by task_id."}, 400))
    
    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message":f"{cls.__name__} {model_id} does not exist."}, 404))
    
    return task 

@tasks_bp.route("", methods=["POST"])
def create_one_task(): 
    request_body = request.get_json()   

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else: # "asc" or None
        tasks = Task.query.order_by(Task.title).all() 
    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response)

@tasks_bp.route("<model_id>", methods=["GET"])
def get_one_task(model_id):
    task = validate_model(Task, model_id)
    return {"task":task.to_dict()}

@tasks_bp.route("/<model_id>", methods=["PUT"])
def update_task(model_id):
    task = validate_model(Task, model_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}, 200

@tasks_bp.route("<model_id>", methods=["DELETE"])
def delete_task(model_id):
    task = validate_model(Task, model_id)
    db.session.delete()
    db.session.commit()

    return {"details" :f'Task {model_id} "{task.title}" successfully deleted'}, 200

@tasks_bp.route("/<model_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(model_id):
    task = validate_model(Task, model_id)
    task.completed_at = datetime.now()
    db.session.commit() 
    call_slack_bot(f"Someone just completed the task {task.title}!")
    return {"task":task.to_dict()}, 200

@tasks_bp.route("/<model_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(model_id):
    task = validate_model(Task, model_id)
    task.completed_at = None 
    db.session.commit()
    return {"task":task.to_dict()}, 200

# My Code:
def call_slack_bot(message):
    URL = "https://slack.com/api/chat.postMessage"
    API_KEY = os.environ.get("TOKEN")
    query_params ={
        "channel" : "task-notifications",
        "text": message
        }
    header = {"Authorization" : API_KEY}
    requests.post(URL, data=query_params, headers=header)

# Thao's Code: 
# def slack_api_call(message):
#     API_KEY = os.environ.get("TOKEN")
#     header = {"Authorization":API_KEY}
#     URL = "https://slack.com/api/chat.postMessage"
#     query_params = {"channel":"task-notifications", "text":message}

#     requests.post(URL, data=query_params, headers=header)

