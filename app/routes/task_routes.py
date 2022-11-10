from flask import Blueprint,request,jsonify,abort, make_response
import requests, json
from app import db
from app.models.task import Task
from sqlalchemy import asc
from sqlalchemy import desc
from app.routes.routes_helper import get_one_obj_or_abort
from app.routes.routes_helper import validate_id
from datetime import date

task_bp = Blueprint("task_bp", __name__, url_prefix ="/tasks")

def post_message_to_slack(text):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'channel': 'task-notifications',
        'text': text}).json()	

def get_one_task_or_abort(task_id):
    matching_task = get_one_obj_or_abort(Task, task_id)
    if not matching_task:
        response_str = f"Task with id {task_id} not found in database"
        abort(make_response(jsonify({"message": response_str}),404))
    return matching_task


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json() 
    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()
    task_dict = new_task.to_dict()
    return jsonify({"task":task_dict}), 201

@task_bp.route("", methods = ["GET"])
def get_task_all():
    title_query = request.args.get("sort") #this will give asc
    if title_query is not None and title_query=="asc":
        tasks = Task.query.order_by(Task.title).all()
    elif title_query is not None and title_query=="desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif title_query is None:
        tasks = Task.query.all()
    response= []
    for task in tasks:
        task_dict = task.to_dict()
        response.append(task_dict)
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods =["GET"])
def get_one_task(task_id):
    validate_id(task_id,'task_id')
    matching_task = get_one_obj_or_abort(Task,task_id)
    if matching_task is None:
        response_message = f"Could not find task with ID {task_id}"
        return jsonify({"message": response_message}), 404
    task_dict = matching_task.to_dict()
    if matching_task.goal_id is not None:
        task_dict["goal_id"]=matching_task.goal_id
    return jsonify({"task": task_dict}), 200
    

@task_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    validate_id(task_id,'task_id')
    task = get_one_task_or_abort(task_id) 
    request_body = request.get_json() #converts json into dictionary
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    task_dict = task.to_dict()
    return jsonify({"task":task_dict}), 200

@task_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def update_task_completed_at(task_id):
    task = get_one_task_or_abort(task_id) 
    if task.completed_at is None:
        task.completed_at = date.today()
    db.session.commit()
    post_message_to_slack("Someone just completed the task "+task.title)
    task_dict = task.to_dict()
    return jsonify({"task":task_dict}),200

@task_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def update_task_mark_incomplete_on_completed_task(task_id):
    task = get_one_task_or_abort(task_id) 
    task.completed_at = None
    db.session.commit()
    task_dict = task.to_dict()
    return jsonify({"task":task_dict}),200
    
@task_bp.route("<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    db.session.delete(chosen_task)
    db.session.commit()
    return jsonify({"details": f'Task {task_id} "Go on my daily walk 🏞" successfully deleted'}),200