from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    

    if "completed_at" not in request_body:  
        new_incomplete_task = Task(
        title = request_body["title"],
        description = request_body["description"])

        db.session.add(new_incomplete_task)
        db.session.commit()
    
        new_incomplete_task_dict = {"id": new_incomplete_task.task_id,
        "title": new_incomplete_task.title,
        "description": new_incomplete_task.description,
        "is_complete": False}

        task_dict = {"task": new_incomplete_task_dict}

    return jsonify(task_dict), 201