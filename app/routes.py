from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task":new_task.to_dict()}), 201


# @tasks_bp.route("", methods=["GET"])
# def get_all_tasks():