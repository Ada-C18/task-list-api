from app import db
from .models.task import Task
from flask import Blueprint, request, make_response, jsonify


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["GET"])
def get_task():
    task_list = Task.query.all()
    response = []

    for task in task_list:
        task_dict = {
            "id" :task.id,
            "title" : task.title,
            "description" : task.description, 
            "is_complete" : False
        }
        response.append(task_dict)

    return jsonify(response), 200

    



@task_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()

    new_task = {
        "title" : request_body["title"],
        "description" : request_body["description"],
    }

    db.session.add(new_task)
    db.session.commit()

