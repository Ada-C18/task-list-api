from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
# from sqlalchemy import asc, desc, select
import datetime
# from datetime import date
import requests
import os


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

# def validate_task_id(task_id):
#     try:
#         task_id = int(task_id)
#     except:
#         abort(make_response({"Message": f"Task {task_id} invalid"}, 400))

#     task = Task.query.get(task_id)
#     if not task:
#         abort(make_response({"Message": f"Task {task_id} not found"}, 404))
#     return task


def post_to_slack(task_title):
    URL = "https://slack.com/api/chat.postMessage"
    HEADER_AUTH = {"Authorization": os.environ.get("SL_TASK_BOT")}
    request_params = {
        "channel": "slack-bot-test-channel",
        "text": f"Someone just completed the task {task_title}"
    }

    response = requests.post(URL, params=request_params, headers=HEADER_AUTH)


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = Task.query

    sort_query = request.args.get("sort")
    if sort_query == "desc":
        task_query = task_query.order_by(Task.title.desc())
    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]
    # tasks_response = []
    # for task in tasks:
    #     # tasks_response.append(task.to_dict())
    #     tasks_response.append(
    #         {
    #             "id": task.task_id,
    #             "title": task.title,
    #             "description": task.description,
    #             "is_complete": bool(task.completed_at),
    #         }
    #     )

    return jsonify(tasks_response), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    # try:
    #     new_task = Task(title=request_body["title"],
    #                     description=request_body["description"],
    #                     completed_at=request_body["completed_at"])
    # except KeyError:
    #     return make_response({
    #         "details": "Invalid data"
    #         }, 400)

    if "title" not in request_body or "description" not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    new_task = Task.from_dict(request_body)
    # new_task = Task(
    #     title=request_body["title"],
    #     description=request_body["description"],
    #     completed_at=request_body["is_complete"]  # Use bool here?
    # )

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201
    # return {
    #     "task": {
    #         "id": new_task.task_id,
    #         "title": new_task.title,
    #         "description": new_task.description,
    #         "is_complete": bool(new_task.completed_at),
    #     }
    # }, 201


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}, 200
    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": bool(task.completed_at),
    #     }
    # }, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200
    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": bool(task.completed_at),
    #     }
    # }, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.datetime.now()
    task_title = task.title

    db.session.commit()

    post_to_slack(task_title)

    return {"task": task.to_dict()}, 200
    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": bool(task.completed_at),
    #     }
    # }, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200
    # return {
    #     "task": {
    #         "id": task.task_id,
    #         "title": task.title,
    #         "description": task.description,
    #         "is_complete": bool(task.completed_at),
    #     }
    # }, 200
