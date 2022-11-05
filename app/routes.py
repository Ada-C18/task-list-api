from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))
        
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

#route functions
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks=Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }), 200
    return jsonify(tasks_response),200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    return jsonify({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
            }}), 200

@tasks_bp.route("", methods=["POST"])
def create_task():  
    request_body = request.get_json()      
    if ("title" not in request_body) or ("description" not in request_body):
        return jsonify({
            "details": "Invalid data"
        }), 400
    else:
        new_task = Task(title=request_body["title"],
                description=request_body["description"])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }}), 201
    

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return jsonify ({
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({
        "details": f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }), 200)