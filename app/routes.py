from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods =["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    for task in tasks:
        tasks_response.append(
            {
                "task id":task.task_id,
                "title": task.title,
                "description": task.description,
                "completed at": task.completed_at
            }
        )
    return jsonify(tasks_response)

@tasks_bp.route("", methods =["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], 
                description=request_body["description"],
                completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.title} successfully created", 201)
