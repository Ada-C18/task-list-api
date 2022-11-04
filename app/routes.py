from flask import Blueprint, jsonify, make_response, abort, request
from app import db
from app.models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))
    
    return model

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json() 

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task": new_task.to_dict()}), 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():  
    sort_query = request.args.get("sort")
    task_query = Task.query

    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())
    if sort_query == "desc":
        task_query = task_query.order_by(Task.title.desc())

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json() #gives us the request body
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200

@tasks_bp.route("/<task_id>/<status>", methods=["PATCH"])
def mark_task_complete(task_id, status):
    task = validate_model(Task, task_id)

    if status == "mark_complete":
        task.completed_at = datetime.utcnow()
    if status == "mark_incomplete":
        task.completed_at = None
    
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200