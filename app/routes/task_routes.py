from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from datetime import date
import os
import requests
from .helper_function import get_one_obj_or_abort

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#--------------------------------helper functions---------------------------

def send_to_slack(task):
    url = "https://slack.com/api/chat.postMessage?channel=task-notifications&text=%22Hello%20World%22&pretty=1"
    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    header = {"Authorization": os.environ.get("SLACK_API_TOKEN")}

    requests.post(url, data= params, headers= header)

#---------------------------POST-------------------------------------------- 
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or\
        "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.create_dict()}), 201 


#--------------------------------------GET------------------------------------
@task_bp.route("", methods=["GET"])
def get_all_tasks():

    sort = request.args.get("sort")
    tasks = ""
    if sort == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks =  Task.query.all()
    response = []
    for task in tasks:
        response.append(task.create_dict())
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    task = get_one_obj_or_abort(Task, task_id)

    return jsonify({"task": task.create_dict()}), 200

#--------------------------------PUT-------------------------
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_values(task_id):
    task = get_one_obj_or_abort(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body or\
        "description" not in request_body:
            return jsonify({"details": "Invalid data"})

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return jsonify({"task": task.create_dict()}), 200

#------------------------PATCH----------------------------------
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = get_one_obj_or_abort(Task, task_id)
    task.completed_at = date.today()
    db.session.commit()
    send_to_slack(task)

    return jsonify({"task": task.create_dict()}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = get_one_obj_or_abort(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return jsonify({"task": task.create_dict()}), 200


#-------------------------DELETE----------------------------
@task_bp.route("/<task_id>", methods=["DELETE"])
def detlete_one_task(task_id):
    task = get_one_obj_or_abort(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200