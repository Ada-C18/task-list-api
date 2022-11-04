from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"], description=request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_dict()}, 201


@task_bp.route("", methods=["GET"])
def get_all_tasks():
    sort = request.args.get("sort")
    sort = getattr(Task.title, sort)() if sort in ("asc", "desc") else None
    return jsonify([t.to_dict() for t in Task.query.order_by(sort).all()])


@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return {"task": task.to_dict()}


@task_bp.route("/<task_id>", methods=["PUT"])
def put_task(task_id):
    form_data = request.get_json()
    task = Task.query.get_or_404(task_id)
    task.title = form_data["title"]
    task.description = form_data["description"]
    db.session.commit()
    return {"task": task.to_dict()}


@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.mark_complete()
    db.session.commit()
    return {"task": task.to_dict()}


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.mark_complete(False)
    db.session.commit()
    return {"task": task.to_dict()}


from psycopg2.errors import InvalidTextRepresentation


@task_bp.errorhandler(404)
def handle_task_not_found(e):
    return {"details": "Task not found"}, 404


@task_bp.errorhandler(InvalidTextRepresentation)
def handle_task_invalid_id(e):
    return {"details": "Task id must be numeric"}, 400


@task_bp.errorhandler(KeyError)
def task_handle_invalid_data(e):
    return {"details": "Invalid data"}, 400
