from flask import Blueprint, request
from . import db
from .models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=['POST'])
def add_task():
    request_body = request.get_json()
    new_task = Task(title=request_body['title'], description=request_body['description'])
    db.session.add(new_task)
    db.session.commit()

    is_complete = False
    if new_task.completed_at:
        is_complete = True
    
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": is_complete
    }}, 201
