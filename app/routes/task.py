from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, make_response, abort

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task


def validate_dict_title_desc(request_body):
    request_body = dict(request_body)
    if not (request_body.get("title", False) and request_body.get("description", False)):
        abort(make_response({"details": "Invalid data"}, 400))


@bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    sort_query = request.args.get("sort")

    task_query = Task.query

    if sort_query:
        task_query = task_query.order_by(Task.title.asc()) if sort_query == "asc" else task_query.order_by(Task.title.desc())

    tasks = task_query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return jsonify(tasks_response)


@bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    task = validate_task(id)
    task_response = {
        "task": task.to_dict()
    }
    return jsonify(task_response)


@bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    validate_dict_title_desc(request_body)
    new_task = Task.task_from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}

    return make_response(jsonify(response_body), 201)


@bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)

    request_body = request.get_json()
    validate_dict_title_desc(request_body)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response_body = {"task": task.to_dict()}

    return jsonify(response_body)


@bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    }

    return jsonify(response_body)
