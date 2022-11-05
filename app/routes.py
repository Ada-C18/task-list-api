from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc, select


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    task_query = Task.query

    sort_query = request.args.get("sort")
    if sort_query == "desc":
        task_query = task_query.order_by(Task.title.desc())
    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())

    tasks = task_query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at),
            }
        )

    return jsonify(tasks_response), 200


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "is_complete" not in request_body:
        return {
            "details": "Invalid data"
        }, 400

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["is_complete"]
    )

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at),
        }
    }, 201


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"Message": f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"Message": f"Task {task_id} not found"}, 404))
    return task


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task_id(task_id)

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
        }
    }, 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at),
        }
    }, 200


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"{task.title}\" successfully deleted"}, 200
