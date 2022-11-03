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

@task_bp.route("", methods = ["GET"])
def get_task():
    tasks = Task.query.all()
    response= []
    
    for task in tasks:
        is_completed = True
        if task.completed_at is None:
            is_completed = False
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_completed
            
        }

        response.append(task_dict)
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods =["GET"])
def get_one_task(task_id):
    tasks = Task.query.all()
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: {task_id} ID must be integer"
        return jsonify({"message": response_str}), 400

    for task in tasks:
        if task_id == task.task_id:
            is_completed = True
            if task.completed_at is None:
                is_completed = False
            task_dict = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_completed
            }
            return jsonify({"task": task_dict}), 200
    response_message = f"Could not find task with ID {task_id}"
    return jsonify({"message": response_message}), 404



    


