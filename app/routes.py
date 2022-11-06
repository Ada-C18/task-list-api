from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

#Get Tasks: Getting Saved Tasks
@tasks_bp.route("", methods=["GET"])
def get_all_task():

    all_tasks = Task.query.all()

    task_response = [task.to_dict() for task in all_tasks]

    return make_response(jsonify(task_response), 200)

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_task(task_id)

    return {"task": {
    "id": task.id,
    "title": task.title,
    "description": task.description,
    "is_complete": False}
}

@tasks_bp.route("", methods=["POST"])

def create_task():
    request_body = request.get_json()

    # guard clause
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400
    new_task= Task(
        title=request_body['title'], 
        description=request_body['description']
        )
    
    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({'task': new_task.to_dict()}), 201)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def edit_task(task_id):

    task = validate_task(task_id)
    request_body = request.get_json()

    task.title=request_body["title"]
    task.description=request_body["description"]

    db.session.commit()

    return make_response(jsonify({'task': task.to_dict()}), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task.id} "{task.title}" successfully deleted'}, 200