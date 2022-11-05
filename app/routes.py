from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response(f"Invalid Request", 400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(
        f"Task {new_task.title} successfully created, 201"
    )

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
        
    return jsonify(tasks_response)