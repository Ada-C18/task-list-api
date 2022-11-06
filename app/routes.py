from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.models.helper import get_one_obj_or_abort

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)
    if new_task.title is None or new_task.description is None:
        response_str = f"Invalid data"
        abort(make_response(jsonify({"details":response_str}), 400))

    db.session.add(new_task)
    db.session.commit()

    task_dict = new_task.to_dict()
    response_body = {
        "task": task_dict
    }

    response = make_response(jsonify(response_body), 201)
    return response

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    response = [task.to_dict() for task in tasks]

    return make_response(jsonify(response), 200)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    task_dict = chosen_task.to_dict()
    response_body = {
        "task": task_dict
    }

    return make_response(jsonify(response_body), 200)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_with_new_vals(task_id):

    chosen_task = get_one_obj_or_abort(Task, task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
    "description" not in request_body:
        return jsonify({"message":"Request must include title and description."}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]

    db.session.commit()

    task_dict = chosen_task.to_dict()
    response_body = {
        "task": task_dict
    }

    return make_response(jsonify(response_body), 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    db.session.delete(chosen_task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{chosen_task.title}\" successfully deleted"}), 200)
