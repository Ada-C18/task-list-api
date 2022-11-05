from app import db
from app.models.task import Task 
from app.models.goal import Goal # Why isn't this accesable?? 
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} is invalid, please search by task_id."}, 400))
    
    task = cls.query.get(model_id)

    if not task:
        abort(make_response({"message":f"{cls.__name__} {model_id} does not exist."}, 404))
    
    return task 

@tasks_bp.route("", methods=["POST"])
def create_one_task(): 
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return {"task" : new_task.to_dict()}, 201

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    name_query = request.args.get("name")
    if name_query:
        task = Task.query.filter_by(name=name_query)
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())
    return jsonify(task_response)

@tasks_bp.route("<model_id>", methods=["GET"])
def get_one_task(model_id):
    task = validate_model(Task, model_id)
    return {"task":task.to_dict()}

@tasks_bp.route("/<model_id>", methods=["PUT"])
def update_task(model_id):
    task = validate_model(Task, model_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}, 200

@tasks_bp.route("<model_id>", methods=["DELETE"])
def delete_task(model_id):
    task = validate_model(Task, model_id)
    db.session.delete(task)
    db.session.commit()

    return {"details" :f'Task {model_id} "{task.title}" successfully deleted'}, 200


    