from datetime import datetime
from flask import Flask, Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from .routes_helper import get_one_obj_or_abort
import os
import requests
task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def create_a_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    # new_task = Task(title=request_body.get("title", None),
    #                 description=request_body.get("description", None))
    if new_task.title is None or new_task.description is None:
        return jsonify({"details": "Invalid data"}),400
    # if "title" not in request_body or \
    #         "description" not in request_body:
    #             return jsonify({"details": "Invalid data"}), 400
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task.to_dict()}), 201

    # return make_response({"task":{
    #                     "id": new_task.task_id,
    #                     "title": new_task.title,
    #                     "description": new_task.description,
    #                     "is_complete": False}}, 201)


@ task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    
    if sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        # tasks = Task.query.all()
        tasks = Task.query.order_by(Task.title).all()

    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200

@ task_bp.route("/<task_id>", methods=["GET"])
def get_one_task_or_abort(task_id):
    # refactored:
    chosen_task = get_one_obj_or_abort(Task, task_id)
    task_dict = {"task" : chosen_task.to_dict()}
    # try:
    #     task_id = int(task_id)
    # except ValueError:
    #     response_str = f"Invalid bike_id: `{task_id}`. ID must be an integer"
    #     abort(make_response(jsonify({"message":response_str}), 400))
    # matching_task = Task.query.get(task_id)
    # if not matching_task:
    #     response_str = f"Task with id `{task_id}` was not found in the database."
    #     abort(make_response(jsonify({"message":response_str}), 404))

    return jsonify(task_dict), 200

@ task_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    chosen_task.is_completed = request_body.get("completed_at", None)

    db.session.commit()

    return jsonify({"task": chosen_task.to_dict()}), 200


@ task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    title = chosen_task.title

    db.session.delete(chosen_task)

    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{title}" successfully deleted'}), 200


@ task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_completed_at(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    # request_body = request.get_json()

    chosen_task.is_completed = True
    # if "completed_at" in request_body:
        # chosen_task.completed_at = request_body["completed_at"]
    chosen_task.completed_at = datetime.now()

    db.session.commit()
    
    API_KEY = os.environ.get("SLACK_TOKEN")
    PATH = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f'Bearer {API_KEY}'}
    params = {"channel": "task-notifications", 
            "text": f"Someone just completed the task {chosen_task.title}"}
    response = requests.get(url=PATH, headers=headers, params=params)
    
    return jsonify({"task": chosen_task.to_dict()}), 200
    # return jsonify({"task": response}), 200

@ task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    
    chosen_task.completed_at = None
    chosen_task.is_completed = False

    db.session.commit()
    return jsonify({"task": chosen_task.to_dict()}), 200