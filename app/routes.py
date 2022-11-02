from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task


task_bp = Blueprint("task", __name__, url_prefix="/tasks")

#helper function to validate task id
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message":f"data type {task_id} is invalid"},400))

    chosen_task = Task.query.get(task_id)
    
    if chosen_task is None:
        abort(make_response({"message":f"Could not find task item with id: {task_id}"},404))

    return chosen_task

##End route to get all tasks
@task_bp.route('', methods=['GET'])
def get_all_tasks():
    title_query_value = request.args.get("title")
    if title_query_value is not None:
        tasks = Task.query.filter_by(title=title_query_value)
    
    else:
        tasks = Task.query.all()
    
    result = []
    
    for task in tasks:
        result.append(task.to_dict())
    
    return jsonify(result), 200

##End route to get one task
@task_bp.route('/<task_id>', methods=['GET'])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify({"task":chosen_task.to_dict()}), 200