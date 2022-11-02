from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(jsonify({"msg": f"{cls.__name__} {model_id} is not valid"}), 400)

    model = cls.query.get(model_id)

    if not model:
        abort(jsonify({"msg": f"{cls.__name__} {model_id} not found"}), 404)

    return model

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

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"msg": f"{new_task.title} added to task list."}), 201

@tasks_bp.route("/<model_id>", methods=["GET"])
def read_one_task_by_id(model_id):
    task = validate_model(Task, model_id)
    return task.to_dict()

    

