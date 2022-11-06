from flask import Blueprint
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import datetime

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"Message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"Message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods =["GET"])
def read_all_tasks(): 
    tasks = Task.query.all()
    tasks_response = []
    
    for task in tasks:
        tasks_response.append(task.to_dict())
    sorting_type = request.args.get("sort")
    if sorting_type == "asc":
        return jsonify(sorted(tasks_response, key = lambda task: task["title"]))
    elif sorting_type == "desc":
        return jsonify(sorted(tasks_response, key = lambda task: task["title"], reverse=True))
    else: 
        return jsonify(tasks_response)

@tasks_bp.route("", methods =["POST"])
def create_task():
    request_body = request.get_json()
    try: 
        new_task = Task(title=request_body["title"], 
                    description=request_body["description"])
    except KeyError:
        abort(make_response({"details":"Invalid data"}, 400))
    

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":new_task.to_dict()}, 201)
    
@tasks_bp.route("/<task_id>", methods =["GET"])
def read_one_task(task_id):
    task = validate_model(Task,task_id)
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    return {"task":task.to_dict()}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    return {"task":task.to_dict()}