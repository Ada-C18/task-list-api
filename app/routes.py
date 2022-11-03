
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

task_bp = Blueprint("task_bp", __name__, url_prefix="/task")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"]
    )
    
    db.session.add(new_task)
    db.session.commit()

    # return make_response (f"Task '{new_task.to_dict()})' successfully created", 201)
    return jsonify({"task": new_task.to_dict()}), 201
