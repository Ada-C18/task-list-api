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
    
    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": True if new_task.completed_at else False
        }
    }

    return jsonify(response_body), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    order = request.args.get("sort")

    if order is None:
        tasks = Task.query.all()
    elif order == "asc":
        tasks = Task.query.order_by(Task.title)
    elif order == "desc":
        tasks = Task.query.order_by(Task.title.desc())

    response_body = []

    for task in tasks:

        response_body.append(
            {
                "id": task.task_id,
                "title":task.title,
                "description": task.description,
                "is_complete": True if task.completed_at else False
            }
        )
    
    return jsonify(response_body), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    response_body = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }

    return jsonify(response_body), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    response_body = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }
    
    db.session.commit()

    return jsonify(response_body), 200


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

    response_body = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }

    return jsonify(response_body), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_one_task_as_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    response_body = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True if task.completed_at else False
        }
    }

    return jsonify(response_body), 200

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