from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route('', methods=['POST'])
def create_one_task():
    request_body = request.get_json()
    new_task= Task(title=request_body['title'],
                description=request_body['description'],
                completed_at=request_body['completed_at'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"msg":f"Successfully created Task with id={new_task.task_id}"}), 201


@task_bp.route('', methods=['GET'])
def get_all_tasks():
    #rating_query_value = request.args.get("rating")
    #if rating_query_value is not None:
    #    tasks = Task.query.filter_by(rating=rating_query_value)
    #else:
    tasks = Task.query.all()
    result = []
    for item in tasks:
        result.append(item.to_dict())  
    return jsonify(result), 200



  