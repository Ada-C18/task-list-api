from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request


bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# Validate
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

# CREATE
@bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify(new_task.to_dict()), 201)

# READ ALL
@bp.route("", methods=["GET"], strict_slashes=False)
def read_all_tasks():
    tasks = Task.query.all()
    tasks_response = [task.resp_all_dict() for task in tasks]

    return jsonify(tasks_response), 200

# READ ONE TASK


@bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify(task.resp_all_dict()), 200

# UPDATE ONE TASK
@bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    return jsonify(task.resp_all_dict()), 200

# #DELETE ONE TASK
@bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return {
        "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
            }
