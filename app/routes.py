from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(({"msg": f"{task_id} is not valid"}), 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response(({"msg": f"{task_id} not found"}), 404))

    return task


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append(task.to_dict())
    
    return jsonify(response), 200


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
            
    except Exception as e:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task_by_id(task_id):
    task = validate_task_id(task_id)
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task_by_id(task_id):
    request_body = request.get_json()
    task = validate_task_id(task_id)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"}), 200