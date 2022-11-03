from flask import Blueprint
from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__,url_prefix="/tasks")

@tasks_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()

    new_task= Task(title=request_body["title"],
                description=request_body["description"]
                # completed_at=request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task":new_task.to_dict()}), 201

