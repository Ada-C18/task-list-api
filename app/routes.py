from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from datetime import datetime


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=None
        )

        db.session.add(new_task)
        db.session.commit()

    except:
        response_body = {
            "details": "Invalid data"
        }

        abort(make_response(jsonify(response_body), 400))
    
    return jsonify(generate_response_body(new_task)), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    order = request.args.get("sort")

    tasks = None
    if order is None:
        tasks = Task.query.all()
    elif order == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif order == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    return jsonify(generate_response_body(tasks)), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return jsonify(generate_response_body(task)), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return jsonify(generate_response_body(task)), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
    }

    return jsonify(response_body), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_one_task_as_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.now()

    db.session.commit()

    return jsonify(generate_response_body(task)), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_one_task_as_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    return jsonify(generate_response_body(task)), 200


#*************** helper functions ***************#

def generate_response_body(tasks):
    """
    Return a list of task-detail dictionaries if @param tasks is a list of Task objects
    Return a single dictionary {"task": task-detail} if @param tasks is a Task object
    """
    if isinstance(tasks, list):
        response = []

        for task in tasks:
            response.append(task.to_dict())

        return response
    
    else:
        return {
            "task": tasks.to_dict()
        }


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response_body = {
            "message": f"Task id {task_id} is invalid."
        }

        abort(make_response(jsonify(response_body), 400))
    
    task = Task.query.get(task_id)

    if task is None:
        response_body = {
            "message": f"Task {task_id} is does not exist."
        }

        abort(make_response(jsonify(response_body), 404))

    return task