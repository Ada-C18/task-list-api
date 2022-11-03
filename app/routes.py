from flask import Blueprint,request,jsonify
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix ="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"]
        
    )
    db.session.add(new_task)
    db.session.commit()
    
    is_completed = True
    if new_task.completed_at is None:
        is_completed = False


    task_dict = {"id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": is_completed
    }

    return jsonify({"task":task_dict}), 201

