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

    response_body = generate_response_body(new_task)
    response = make_response(jsonify(response_body), 201)
    return response

def generate_response_body(task):
    task_dict = task.to_dict()

    response_body = {
        "task": task_dict
    }

    return response_body


