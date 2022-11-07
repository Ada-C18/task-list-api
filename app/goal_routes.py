from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort


goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

@goals_bp.route("", methods=["GET"])
def get_all_tas():
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