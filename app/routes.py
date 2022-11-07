from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":f"{new_task}"}, 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

def validate_task(task_id):
    task = Task.query.get(task_id)
   
    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))
    
    return task

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    chosen_task = validate_task(task_id)

    return chosen_task.to_dict()

# @tasks.bp.route("/<task_id>", methods=["PUT"])
# def 