from datetime import date
import os
from app import db
from app.models.task import Task
from flask import Blueprint, abort, jsonify, make_response, request
import requests


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        return abort(make_response({"message": f"task {task_id} has an invalid task_id"}), 400)

    query_result = Task.query.get(task_id)

    if not query_result:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return query_result


def slack_call(task): 
    # route
    SLACK_BOT_ROUTE = "https://slack.com/api/chat.postMessage"
    
    # query params
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    
    # Header
    headers = {
        "Authorization": os.environ.get("SLACK_BOT_TOKEN")
    }
    
    # method
    requests.post(SLACK_BOT_ROUTE, params=query_params, headers=headers)


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    is_valid = Task.is_valid(new_task)
    if not is_valid:
        return make_response(jsonify({ "details": "Invalid data"}), 400)
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": Task.to_dict(new_task)})), 201

@tasks_bp.route("/<task_id>", methods=["GET"])
def one_saved_task(task_id):
    task = validate_task(task_id)

    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    title_query = request.args.get("sort")
    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
        
    elif title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
        
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = validate_task(task_id)
    task.completed_at = date.today()
    
    db.session.commit()
    
    slack_call(task)
    
    return make_response(jsonify({"task": Task.to_dict(task)})), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    
    db.session.add(task)
    db.session.commit()

    return make_response(jsonify({"task": Task.to_dict(task)})), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(jsonify({"task": Task.to_dict(task)})), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted" })), 200

