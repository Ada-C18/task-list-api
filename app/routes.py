from flask import Blueprint, jsonify, make_response, request, abort
from .models.task import Task
from app import db

# ===================
# BLUEPRINTS
# ===================

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# ===================
# HELPER FUNCTIONS
# ===================

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task

# ===================
# ROUTES
# ===================

@tasks_bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.new_instance_from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        return {"task": new_task.create_dict()}, 201
        
    except KeyError:
        return {"details": "Invalid data"}, 400

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.create_dict() for task in tasks]

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    response = {"task": task.create_dict()}
    return make_response(response)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    task.update(request_body)

    db.session.commit()

    return {"task": task.create_dict()}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task.task_id} \"{task.title}\" successfully deleted"}