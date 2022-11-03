from app import db
from app.models.task import Task
from flask import abort, Blueprint, jsonify, make_response, request

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

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
