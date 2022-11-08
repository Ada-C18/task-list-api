from flask import Flask, Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db

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


@tasks_bp.route("", methods=["POST"])
def create_task():
    '''Creates a new Task record. Entering a date for "completed_at" is optional.'''
    request_body = request.get_json()
    try:
        new_task = Task(
            title=request_body["title"], 
            description=request_body["description"],
            completed_at=request_body["completed_at"]
            )
    except KeyError:
        try:
            new_task = Task(
                title=request_body["title"], 
                description=request_body["description"],
                )
        except KeyError:
            return {"details": "Invalid data"}, 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": Task.task_response(new_task)}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_param = request.args.get("sort")
    sort_func = getattr(Task.title, sort_param)() if sort_param in ("asc", "desc") else None
    all_tasks = Task.query.order_by(sort_func).all()

    return jsonify([task.to_dict() for task in all_tasks])


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()

    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    validated_task = validate_model(Task, task_id)
    task = Task.query.get(validated_task.task_id)

    task.mark_complete()
    db.session.commit()
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    validated_task = validate_model(Task, task_id)
    task = Task.query.get(validated_task.task_id)

    task.mark_complete(False)
    db.session.commit()
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}