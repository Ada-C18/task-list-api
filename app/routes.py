from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request,abort
from sqlalchemy import asc, desc 
import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()
    new_task = Task.from_dict(request_body) 

    db.session.add(new_task)
    db.session.commit()

    task_dict = {}
    task_dict["task"] = {"id":new_task.task_id, "title": new_task.title,"description":new_task.description, "is_complete":bool(new_task.completed_at)}

    return make_response(jsonify(task_dict), 201) 

@tasks_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        if "asc" in sort_query: 
            tasks = Task.query.order_by(Task.title.asc())
        elif "desc" in sort_query: 
            tasks = Task.query.order_by(Task.title.desc()) 
    else: 
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response) 
    

def validate_model(cls, model_id):
    try: 
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400)) 

    model = cls.query.get(model_id)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404)) 

    return model

@tasks_bp.route("/<task_id>", methods = ["GET"])
def get_one_task(task_id):
    task = validate_model(Task,task_id)

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    return make_response(jsonify(task_dict), 200) 

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()

    task.update(request_body) 
    db.session.commit()

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    return make_response(jsonify(task_dict), 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task,task_id)

    db.session.delete(task)
    db.session.commit()
    dict = {"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}

    return make_response(jsonify(dict), 200)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = datetime.datetime.now()

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    db.session.commit()

    return make_response(jsonify(task_dict), 200)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task,task_id)
    task.completed_at = None 

    task_dict = {}
    task_dict["task"] = {"id":task.task_id, "title": task.title,"description":task.description, "is_complete":bool(task.completed_at)}

    db.session.commit()

    return make_response(jsonify(task_dict), 200)
