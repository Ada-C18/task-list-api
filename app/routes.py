from flask import Blueprint, jsonify
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


