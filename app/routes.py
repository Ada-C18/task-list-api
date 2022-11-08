from flask import Blueprint, request, jsonify, make_response, abort
from app import db 
from app.models.task import Task
from app.models.goal import Goal
from datetime import date
import logging
import os
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)

task_list_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")


#READ all tasks 
@task_list_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        tasks = get_tasks_sorted(sort_query)
    else:
        tasks = Task.query.all()

    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200

#READ one task
@task_list_bp.route("/<task_id>", methods= ["GET"])
def get_one_task(task_id):
    task = validate_model_id(Task, task_id)
    if task.goal_id is None:
        response = {"task": task.to_dict()}
    else:
        response = {"task": task.to_dict_with_goal_id()}

    return jsonify(response), 200

#CREATE new task
@task_list_bp.route("", methods = ["POST"])
def create_new_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}
    return jsonify(response_body), 201


#UPDATE task
@task_list_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_model_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    response_body = {"task": task.to_dict()}

    return jsonify(response_body)

#DELETE task
@task_list_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = validate_model_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200 

#UPDATE mark complete
@task_list_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
def mark_complete(task_id):
    task = validate_model_id(Task, task_id)

    task.completed_at = date.today()
    task.is_complete = True
    response = {"task": task.to_dict()}

    db.session.commit()
    send_completed_msg(task)

    return jsonify(response), 200



#UPDATE mark incomplete
@task_list_bp.route("/<task_id>/mark_incomplete", methods = ["PATCH"])
def mark_incomplete(task_id):
    task = validate_model_id(Task, task_id)
    task.incomplete = False
    task.completed_at = None
    response = {"task": task.to_dict()}
    
    db.session.commit()
    return jsonify(response), 200



#================== Helper Functions=================
def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    chosen_object = cls.query.get(model_id)

    if not chosen_object:
        abort(make_response({"message": f"{cls.__name__.lower()} {model_id} not found"}, 404))

    return chosen_object

#get sorted tasks helper function
def get_tasks_sorted(sort_query):
    if sort_query == "desc": 
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.order_by(Task.title).all()

    return(tasks)

#PATCH slackbot for mark complete
def send_completed_msg(task):
    try:
        result = client.chat_postMessage(
            channel = os.environ.get("CHANNEL_ID"),
            text= f"Someone just completed the task {task.title}"
        )
    except SlackApiError as error:
        logger.error(f"Error posting message: {error}")