from app import db
from datetime import datetime
from flask import abort, Blueprint, jsonify, make_response, request
from app.models.task import Task
from app.routes.helper_functions import validate_model
import os
import requests


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

# The routes below are ordered by CRUD

#==============================
#       HELPER FUNCTIONS
#==============================
def slack_bot_post_task_notification(message):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")
    CHANNEL = "C04AEBE3LD7"
    
    req_headers={"Authorization": SLACK_API_KEY}
    req_data={
            "channel": CHANNEL,
            "text": message
            }

    requests.post(url=PATH,
                headers=req_headers,
                data=req_data
                )

#==============================
#         CREATE TASK
#==============================
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if "completed_at" not in request_body:
        request_body["completed_at"]=None

    new_task = Task.new_instance_from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    task_response = {"task": new_task.create_dict()}

    return make_response(jsonify(task_response), 201)


#==============================
#        READ ALL TASKS
#==============================
@task_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")

    if sort_query=="asc":
        tasks=Task.query.order_by(Task.title.asc())
    elif sort_query=="desc":
        tasks=Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    tasks_response = [task.create_dict() for task in tasks]

    return make_response(jsonify(tasks_response), 200)

#==============================
#        READ ONE TASK
#==============================
@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    task_dict = task.create_dict()
    if task.goal_id:
        task_dict["goal_id"] = task.goal_id
        
    task_response = {"task": task_dict}
    return make_response(jsonify(task_response), 200)

#==============================
#         UPDATE TASK
#==============================
@task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()

    task_response = {"task": task.create_dict()}
    return make_response(jsonify(task_response), 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_completed_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    task.is_complete_check()
    db.session.commit()

    slack_bot_post_task_notification(f"Someone just completed the task {task.title}")
    task_response = {"task": task.create_dict()}
    return make_response(jsonify(task_response), 200)

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_incompleted_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    task.is_complete_check()
    db.session.commit()

    task_response = {"task": task.create_dict()}
    return make_response(jsonify(task_response), 200)

#==============================
#         DELETE TASK
#==============================
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    task_response = {"details": f'Task {task.id} "{task.title}" successfully deleted'}
    return make_response(jsonify(task_response), 200)
