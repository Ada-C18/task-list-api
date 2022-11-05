from app import db
from app.models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    task = cls.query.get(model_id)
    if not task:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response(f"Invalid Request", 400)
    
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task":new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
        
    return jsonify(tasks_response)

@tasks_bp.route("/<model_id>", methods= ["GET"])
def read_one_task(model_id):
    task = validate_model(Task, model_id)
    return {"task":task.to_dict()}

@tasks_bp.route("/<model_id>", methods= ["PUT"])
def update_task(model_id):
    task = validate_model(Task, model_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}, 200
