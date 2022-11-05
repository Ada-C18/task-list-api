from flask import Blueprint, jsonify, abort, make_response, request
from app.models.task import Task
from app import db



task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id=int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__}{model_id} invalid"}, 400))
    model =  cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} was not found"}, 404))
    return model

@task_bp.route("", methods = ["GET"])
def read_all_tasks():
    tasks = Task.query.all()
    tasks_data=[task.to_dict() for task in tasks]

    return jsonify(tasks_data)

@task_bp.route("/<task_id>", methods = ["GET"])
def read_one_task(task_id):

    task = validate_model(Task, task_id)
    
    return {"task":task.to_dict()}

@task_bp.route("", methods = ["POST"])
def create_task():
    try:
        request_body = request.get_json()
        new_task = Task.from_dict(request_body)
    except:
        abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_task)
    db.session.commit()
    return {"task":new_task.to_dict()}, 201

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return {"task":task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()
    return make_response(jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}),200)
    