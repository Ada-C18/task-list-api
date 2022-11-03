from flask import Blueprint
from app import db
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    '''
    POST method - allows client to post tasks to the tasks record
    '''
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])#,

    db.session.add(new_task)
    db.session.commit()

    response_body = {
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": True if new_task.completed_at is not None else False
        }
    }

    return make_response(response_body, 201)
