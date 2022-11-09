from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task
from datetime import date
import os
import requests


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("",methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at = None
            )
    except:
        return jsonify({
        "details": "Invalid data"
    }), 400

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.to_dict_task()), 201

@task_bp.route("",methods=["GET"])
def get_all_tasks():
    title_query_value = request.args.get("title") #thing after .args.get is equal to what comes after the ? (ex. tasks?title, tasks?sort)
    ascending_order = request.args.get("sort") #variable stores result which is what comes after the = (ex. tasks?sort=asc, tasks?sort=desc) the asc or desc will be stored in ascending_order variable
    
    tasks = Task.query #.query is not currently doing anything just gets stored, filter_by and order_by are just specifying how/which data to get, and query.all() is the thing that makes it take action and retrieve the data from the database
    
    if title_query_value is not None:
        tasks = tasks.filter_by(title=title_query_value)
    if ascending_order == "asc":
        tasks = tasks.order_by(Task.title.asc())
    if ascending_order == "desc":
        tasks = tasks.order_by(Task.title.desc())

    result = []
    for task in tasks.all():
        result.append(task.to_dict_all_tasks())
    return jsonify(result), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify(chosen_task.to_dict_task()), 200

def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"message":f"Invalid data type {task_id}"}, 400))

    chosen_task = Task.query.get(task_id)

    if chosen_task is None:
        return abort(make_response({"message": f"Could not find a task with id {task_id}"}, 404))

    return chosen_task

@task_bp.route("/<task_id>",methods=["PUT"])
def update_one_task_id(task_id):
    update_task = get_task_from_id(task_id)
    request_body = request.get_json()

    try:
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
    except KeyError:
        return jsonify({"details":f"Invalid data"}), 400

    db.session.commit()
    return jsonify(update_task.to_dict_task()), 200

@task_bp.route("/<task_id>/mark_complete",methods=["PATCH"])
def update_one_task_complete(task_id):
    update_task_mark_complete = get_task_from_id(task_id)

    update_task_mark_complete.completed_at = date.today()
    
    db.session.commit()

    channel_id = "task-notifications"
    slack_path = "https://slack.com/api/chat.postMessage"
    SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    parameters = {"channel":channel_id, "text": f"Someone just completed the task {update_task_mark_complete.title}"}

    requests.get(url=slack_path, headers=headers, params=parameters)

    return jsonify(update_task_mark_complete.to_dict_task()), 200

@task_bp.route("/<task_id>/mark_incomplete",methods=["PATCH"])
def update_one_task_incomplete(task_id):
    update_task_mark_incomplete = get_task_from_id(task_id)

    update_task_mark_incomplete.completed_at = None

    db.session.commit()
    return jsonify(update_task_mark_incomplete.to_dict_task()), 200

@task_bp.route("/<task_id>",methods=["DELETE"])
def delete_one_task(task_id):
    task_to_delete=get_task_from_id(task_id)
    
    db.session.delete(task_to_delete)
    db.session.commit()
    
    return jsonify({"details":f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'}), 200
