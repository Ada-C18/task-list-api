from flask import Blueprint, jsonify, abort, make_response
from app.models.task import Task

#make a blueprint
task_bp = Blueprint("task_bp", __name__, url_prefix = "/tasks")

@task_bp.route("", methods = ["GET"])
def get_all_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        task_dict = task.make_dict()
        response.append(task_dict)
    return jsonify(response), 200


@task_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    task_dict = task.make_dict()
    return make_response({"task": task_dict}, 200)
    

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Task {task_id} must be an integer"
        abort(make_response({"message": response_str}, 400))
    task = Task.query.get(task_id)
    if not task:
        response_str = f"Task {task_id} not found"
        abort(make_response({"message": response_str}, 404))
    return task


