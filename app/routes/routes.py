import json
from flask import abort, Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task
from sqlalchemy import desc, asc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


# error handling
def validate_task(task_id):
    # invalid task id
    try:
        task_id = int(task_id)
    except:
        abort(make_response({{"message": f"Invalid task id {task_id}."}}, 400))

    task = Task.query.get(task_id)

    # task not found
    if not task:
        abort(make_response({"message": f"Task {task_id} not found."}, 404))

    return task


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or \
            "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=None,
    )

    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": new_task.to_dict()
    }

    return response, 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    # ADDING FUNCTIONALITY
    # functionality: sort task by title -> Add title query param
    order_param = request.args.get("sort")

    if order_param is None:
        tasks = Task.query.all()
    elif order_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif order_param == "asc":
        tasks = Task.query.order_by(Task.title.asc())

    # tasks_response = []
    # for task in tasks:
    #     task_dict = task.to_dict()
    #     tasks_response.append(task_dict)

    # list comprehension syntax
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)


# Create GET route for 1 task
@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_bike(task_id):
    chosen_task = validate_task(task_id)

    response = {
        "task": chosen_task.to_dict()
    }

    return response, 200


# Update Task
@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    response = {
        "task": task.to_dict()
    }

    db.session.commit()

    return jsonify(response), 200
    # return response, 200 # jsonify needed here?


# fix delete ROUTE -> 400 not working
@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
    }

    return jsonify(response), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_to_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.utcnow()

    updated_task = task.to_dict()

    db.session.commit()

    response = {
        "task": updated_task
    }

    return response, 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_to_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    updated_task = task.to_dict()
    response = {
        "task": updated_task
    }

    return response, 200
