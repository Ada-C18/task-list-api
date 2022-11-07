from app import db
from .models.task import Task
from flask import Blueprint, request, make_response, jsonify


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.route("", methods=["GET"])
def get_all_task():
    response = []
    task_list = Task.query.all()
    for task in task_list:
        response.append(task.to_dict())
    return jsonify(response), 200

@task_bp.route("/<id>", methods=["GET"])
def get_one_task(id):
    try:
        task = Task.query.get(id)
        response = {"task" : task.to_dict()}
    except:
        return jsonify("Task Not Found"), 404
    return jsonify(response), 200
    

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    new_task = Task (title = request_body["title"],
        description = request_body["description"]) 

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task" : new_task.to_dict()}, 201)

    


