from app import db
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details": "Invalid data"}), 400)

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"msg":f"Task {task_id} not found"}, 404))
        # f"{cls.__name__} {model_id} not found"}, 404))

    return task

def get_task_from_id(task_id):
    # try:
    #     breakfast_id = int(breakfast_id)
    # except ValueError:
    #     return abort(make_response({"msg": f"invalid data type: {breakfast_id}"}, 400))
    chosen_task = Task.query.get(task_id)
    if chosen_task is None:
        return abort(make_response({"msg": f"Could not find task item with id: {task_id}"}, 404))
    return chosen_task

@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
        # completed_at=request_body["completed_at"]
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task":new_task.to_dict()}), 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    tasks = Task.query.all()

    result = []
    for task in tasks:
        result.append(task.to_dict())

    return jsonify(result), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_task_from_id(task_id)
    return jsonify({"task":chosen_task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.completed_at = request_body["completed_at"]
    db.session.commit()

    return jsonify({"task":task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    task_title = task.title

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task_title}" successfully deleted'}), 200
    