from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db


task_bp = Blueprint("task", __name__, url_prefix = "/tasks")

@task_bp.route('', methods=["GET"])
def get_all_tasks():
    title_query_value = request.args.get("title") 
    # It's better to check for None rather than check for falsey, in case we are checking for value equal to 0 or False.
    if title_query_value is not None: 
        tasks = Task.query.filter_by(title = title_query_value)
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:    
        response.append(task.to_dict())

    return jsonify(response), 200



