from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    return jsonify(tasks_response)

@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(f"Task {new_task.title} successfully created."), 201)

