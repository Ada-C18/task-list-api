from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from datetime import datetime


import requests
import os

task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"]
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    query_vlaue = request.args.get("sort")
    if query_vlaue == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif query_vlaue == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        task = Task.query.all()

    response = []
    for task in tasks:
        response.append(task.to_dict())
    return make_response(jsonify(response), 200)

# helper function


def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({'msg': f'Invalid id: {task_id}.ID must be an integer '}, 400))

    matching_task = Task.query.get(task_id)
    if matching_task is None:
        return abort(make_response({'msg': f'could not find task item with id: {task_id}'}, 404))

    return matching_task


@ task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    return make_response(jsonify({"task": chosen_task.to_dict()}), 200)


@ task_bp.route("/<task_id>", methods=["PUT"])
def update_task_with_new_vals(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    request_body = request.get_json()
    if "title" not in request_body or\
            "description" not in request_body:
        return jsonify({"msg": "Request must include title, description"}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]

    db.session.commit()
    return make_response(jsonify({"task": chosen_task.to_dict()}), 200)


@ task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    db.session.delete(chosen_task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{chosen_task.title}" successfully deleted'}), 200


@ task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = get_one_task_or_abort(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()
    path = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f'Bearer {os.environ.get("API_KEY")}'}
    query_params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    requests.post(path, params=query_params, headers=headers)
    return jsonify({"task": task.to_dict()}), 200


@ task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = get_one_task_or_abort(task_id)
    task.completed_at = None

    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200
