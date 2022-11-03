from flask import Blueprint,jsonify, abort, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp",__name__, url_prefix="/task")



@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        completed_at = request_body["completed_at"]
    )

    db.session.add(new_task)

    db.session.commit()

    return {"task":{
        "id":new_task.id,
        "title":new_task.title,
        "description":new_task.description,
        "is_complete":new_task.is_complete
    }
    }, 201

