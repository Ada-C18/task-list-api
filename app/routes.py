from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])

def add_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["A Brand New Task"],
        description=request_body["Test Description"],
        completed_at=request_body["null"]

    )

    db.session.add(new_task)
    db.session.commit()

    return {"id": new_task.id}, 201