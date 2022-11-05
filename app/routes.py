from flask import Blueprint, jsonify, request, make_response, request
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

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



