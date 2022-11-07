from flask import Blueprint, jsonify, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()
    
        task = Task(title = request_body["title"], description = request_body["description"])

        db.session.add(task)
        db.session.commit()

        response_body = {"task": task.to_dict()}

        return make_response(jsonify(response_body), 201)

    elif request.method == "GET":
        tasks = Task.query.all()
        response_body = []
        for task in tasks:
            response_body.append(task.to_dict())
        return make_response(jsonify(response_body), 200)

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = Task.query.get(task_id)

    return make_response(jsonify(task.to_dict()))