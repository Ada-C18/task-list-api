from flask import Blueprint, request, jsonify, abort, make_response
from . import db
from .models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg": f"Task {task_id} invalid"}, 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"msg": f"Task {task_id} not found"}, 404))
    return task

@tasks_bp.route("", methods=['POST'])
def add_task():
    request_body = request.get_json()
    new_task = Task(title=request_body['title'], description=request_body['description'])
    db.session.add(new_task)
    db.session.commit()

    is_complete = False
    if new_task.completed_at:
        is_complete = True
    
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": is_complete
    }}, 201

@tasks_bp.route("", methods=['GET'])
def get_tasks():
    tasks = Task.query.all()

    response = []
    for task in tasks:
        is_complete = False
        if task.completed_at:
            is_complete = True
        response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
        })
    
    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)

    is_complete = False
    if task.completed_at:
        is_complete = True
    return {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete}, 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except:
        raise KeyError("Either task title or description is missing from your input")
    db.session.commit()

    is_complete = False
    if task.completed_at:
        is_complete = True
    return {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete}, 200

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    return make_response(f"Task {title} successfully deleted"), 200