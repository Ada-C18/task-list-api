from flask import abort, Blueprint, jsonify, make_response, request
from app import db

from app.models.task import Task

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route('', methods=['GET'])
def get_all_tasks():
    rating_query_value = request.args.get("title") # has to be string
    if rating_query_value is not None: # ! rather checking not None
        tasks = Task.query.filter_by(rating=rating_query_value)
    else:
        tasks = Task.query.all()

    result = []
    for item in tasks:
        result.append(item.to_dict())

    return jsonify(result), 200
