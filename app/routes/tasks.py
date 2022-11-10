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
