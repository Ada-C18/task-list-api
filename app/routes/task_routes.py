from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Validate


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


# CREATE
@bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.from_dict(request_body)
    except:
        abort(make_response(jsonify({
            "details": "Invalid data"}), 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)


# READ ALL
@bp.route("", methods=["GET"], strict_slashes=False)
def read_all_tasks():
    sort_query = request.args.get("sort")

    task_query = Task.query

    if sort_query == "asc":
        task_query = task_query.order_by(asc(Task.title))
    if sort_query == "desc":
        task_query = task_query.order_by(desc(Task.title))

    tasks = task_query.all()
    response_body = [task.to_dict() for task in tasks]

    return make_response(jsonify(response_body), 200)


# READ ONE TASK
@bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    if not task.goal_id:
        return jsonify({"task": task.to_dict()}), 200
    else:
        return jsonify({"task": task.to_dict_with_goal_id
        ()}), 200

# UPDATE ALL ONE TASK


@bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200

# UPDATE PART OF ONE TASK - COMPLETE


@bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    # Send to SlackBot - consider using a helper function here
    load_dotenv()
    PATH = os.environ.get("COMPLETE_PATH")
    PASS = os.environ.get("API_TOKEN")
    query_params = {'text': f"Someone just completed the task {task.title}",
                    'channel': '#task-notifications'} 
    requests.post(PATH,
                  json=query_params,
                  headers={
                      'Content-type': 'application/json',
                      'Authorization': PASS
                  })

    return jsonify({"task": task.to_dict()}), 200

# UPDATE PART OF ONE TASK - INCOMPLETE

@bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200


# #DELETE ONE TASK
@bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({
        "details": f"Task {task.task_id} \"{task.description}\" successfully deleted"}),
        200)
