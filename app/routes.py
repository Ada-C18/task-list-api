from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
from datetime import datetime

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

def validate_info(request_obj):
    obj_keys = request_obj.keys()
    if 'title' not in obj_keys or 'description' not in obj_keys:
        abort(make_response({"details": "Invalid data"}, 400))
    else:
        return request_obj


def wrap_task(task_obj):
    return {"task": task_obj}

@tasks_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    request_body = validate_info(request_body)
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    response_body = wrap_task(new_task.to_dict())

    return make_response(response_body, 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return wrap_task(task.to_dict())

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return wrap_task(task.to_dict())

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    response_body = f"Task {task_id} \"{task.title}\" successfully deleted"
    db.session.delete(task)
    db.session.commit()

    return make_response({"details": response_body})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.utcnow()
    
    db.session.commit()
    return wrap_task(task.to_dict())
    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    result = task.to_dict()
    result['is_complete'] = False

    db.session.commit()
    return wrap_task(result)