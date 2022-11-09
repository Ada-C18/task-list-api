from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from sqlalchemy import desc
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model

# def validate_task_data(task_data):
#     try:
#         assert "description" in task_data
#         assert "title" in task_data
#     except:
#         abort(make_response({"details": "Invalid data"}), 400)

@tasks_bp.route("", methods = ["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return make_response(jsonify({"task": task.to_dict()}), 200)

@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()
    
    if "description" not in request_body or "title" not in request_body:
        #also check for completed_at?
        return make_response(jsonify({"details": "Invalid data"}), 400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@tasks_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}), 200)

@tasks_bp.route("/<task_id>/<status>", methods = ["PATCH"])
def mark_completion(task_id, status):
    task = validate_model(Task, task_id)
    if status == "mark_complete":
        task.completed_at = datetime.utcnow()
    elif status == "mark_incomplete":
        task.completed_at = None
    db.session.commit()
    return make_response(jsonify({"task": task.to_dict()}), 200)

@tasks_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)
