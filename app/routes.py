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
    request_body = request.get_json()
    if not "title" in request_body or not "description" in request_body:
        return make_response({"details":"Invalid data"}, 400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({
        "task": {
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }, 201)

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    all_tasks = Task.query.all()
    response_body = []

    for task in all_tasks:
        response_body.append(
            {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False if task.completed_at is None else True
            }
        )
    return jsonify(response_body)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False if task.completed_at is None else True
    }}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.update(request_body)
    db.session.commit()

    return {"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": False if task.completed_at is None else True
    }}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}