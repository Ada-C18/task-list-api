from os import abort
from datetime import datetime
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, abort, make_response
import sqlalchemy

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    if not request.is_json:
        return {"msg": "Missing JSON request body"}, 400

    request_body = request.get_json()
    try:
        title = request_body["title"]
        description = request_body["description"]
        completed_at = request_body["completed_at"]

    except KeyError:
        return {"details": "Invalid data"}, 400
        
        # if "title" not in request_body or "description" not in request_body or

    new_task = Task(
        title=title,
        # request_body["title"],
        description=description,
        # request_body["description"],
        # request_body["completed_at"]
        completed_at=completed_at
        if request_body["completed_at"] is not None else None
    )

    db.session.add(new_task)
    db.session.commit()

    rsp = {"task": new_task.get_dict()}

    return jsonify(rsp), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    tasks = Task.query.all()

    if sort_query == "asc":
        tasks = Task.query.order_by(sqlalchemy.asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(sqlalchemy.desc(Task.title))

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.get_dict())

    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    rsp = {"task" : task.get_dict()}

    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    if not request.is_json:
        return {"msg" : "Missing JSON request body"}, 400

    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except KeyError:
        return {
            "msg" : "Update failed due to missing data. Title, Description are required!"
        }, 400

    db.session.commit()

    rsp = {"task" : task.get_dict()}
    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    rsp = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    return jsonify(rsp), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    
    # channel_id = "C049FQLJTBN"
    # SlackUrl = 'https://slack.com/api/chat.postMessage'
    

    db.session.commit()

    rsp = {"task": task.get_dict()}
    return jsonify(rsp), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None

    db.session.commit()

    rsp = {"task": task.get_dict()}
    return jsonify(rsp), 200


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        rsp = {"msg": f"Task with id #{task_id} is invalid."}
        abort(make_response(rsp, 400))
    
    task = Task.query.get(task_id)

    if not task:
        rsp = {"msg": f"Task with id #{task_id} is not found!"}
        abort(make_response(rsp, 404))
    return task
