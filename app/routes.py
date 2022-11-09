from app import db
from app.models.task import Task
from datetime import datetime
from flask import Blueprint, abort, jsonify, make_response, request
from sqlalchemy import asc, desc

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task.from_dict(request_body)
    
    db.session.add(new_task)
    db.session.commit()

    return make_response({"task": new_task.to_dict()}, 201)

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if sort_query == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif sort_query == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return make_response(jsonify(task_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)




