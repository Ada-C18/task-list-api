from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])

def add_task():
    request_body = request.get_json()

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
    ) # could do a conditional iif completed_at = null in the request, update the task object with is_complete = False


    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

@tasks_bp.route("", methods=["GET"])


def get__saved_tasks():
    name_param = request.args.get("name")

    if name_param is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(name=name_param)

    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_bike(task_id):
    chosen_task = get_one_obj_or_abort(Task,task_id)

    task_dict = chosen_task.to_dict()

    return jsonify(task_dict), 200

''' def get_tasks():
    title_param = Task.query.all()

    if title_param is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(title=title_param)
    
    response = []
    for task in tasks:
        task_dict = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
        response.append(task_dict)
    return jsonify(response), 200 '''