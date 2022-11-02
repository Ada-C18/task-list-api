from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")
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