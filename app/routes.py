from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# def make_task_dict(task):
    
#     task_dict = {
#         "id": task.task_id,
#         "title": task.title,
#         "description": task.description,
#     }



    
@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        })
    return jsonify(tasks_response)

@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = None)
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
            }
        }), 201)

