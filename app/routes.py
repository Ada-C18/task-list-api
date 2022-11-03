from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response, abort

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
        #completed_at=request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task":new_task.to_dict()}), 201


@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    rating_query_value = request.args.get("title")

    if rating_query_value is not None:
        tasks = Task.query.filter_by(rating=rating_query_value)
    else:
        tasks = Task.query.all()
    
    result = []

    for item in tasks:
        result.append(item.to_dict())
    
    return jsonify(result), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):


#helper function