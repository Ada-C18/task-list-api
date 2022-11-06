from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, make_response, abort
from sqlalchemy import asc, desc, select
from datetime import datetime as dt

bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"details":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"details":f"{cls.__name__} {model_id} not found"}, 404))

    return model

@bp.route("", methods=["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.from_dict(request_body)

        db.session.add(new_task)
        db.session.commit()

        task_dict = new_task.to_dict()

        return make_response(jsonify({
            "task": task_dict}), 201)
            
    except:
        abort(make_response({"details": "Invalid data"}, 400))

@bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    task_query = Task.query
    if sort_query == "asc":
        task_query = Task.query.order_by(Task.title.asc())
    if sort_query == "desc":
        task_query = Task.query.order_by(Task.title.desc())
    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response), 200

@bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)

    return make_response(jsonify({
            "task": task.to_dict()
    }))

@bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return make_response(jsonify({
        "task": task.to_dict()
    }))

@bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }))

@bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_to_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = dt.utcnow()
    task.is_complete = True

    db.session.commit()

    return make_response(jsonify({
        "task": task.to_dict()
    }))

@bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_to_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    return make_response(jsonify({
        "task": task.to_dict()
    }))