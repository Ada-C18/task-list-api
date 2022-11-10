from flask import request, jsonify
from app import db
from app.models.task import Task
from . import tasks


@tasks.route("", methods=["POST"])
def post_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"], description=request_body["description"]
    )
    db.session.add(new_task)
    db.session.commit()
    return {"task": new_task.to_dict()}, 201


@tasks.route("", methods=["GET"])
def get_all_tasks():
    by = request.args.get("by")
    by = getattr(Task, by) if by in ("title", "task_id") else Task.title
    sort = request.args.get("sort")
    order_by = getattr(by, sort)() if sort in ("asc", "desc") else None

    title = request.args.get("title")
    filter = Task.title.like(f"%{title}%") if title else None

    query = Task.query
    query = query.filter(filter) if title else query
    query = query.order_by(order_by) if sort else query

    return jsonify([t.to_dict() for t in query.all()])


@tasks.route("/<task_id>", methods=["PUT"])
def put_task(task_id):
    form_data = request.get_json()
    task = Task.query.get_or_404(task_id)
    task.update(**form_data)
    db.session.commit()
    return {"task": task.to_dict()}


@tasks.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {task.task_id} "{task.title}" successfully deleted'}


@tasks.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.mark_complete()
    db.session.commit()
    return {"task": task.to_dict()}


@tasks.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def incomplete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.mark_complete(False)
    db.session.commit()
    return {"task": task.to_dict()}
