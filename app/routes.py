from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from sqlalchemy import asc, desc
from app import db

task_db = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        if task_id:
            abort(make_response({"message": f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} is not found"}, 404))
    
    return task
    
@task_db.route("", methods=["POST"])
def create_tasks():
    
    request_body = request.get_json()
    
    task_list = ["description", "title"]
    
    for task in task_list:
        if task not in request_body:
            abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task(description=request_body["description"],
        title=request_body["title"])

    db.session.add(new_task)
    db.session.commit()
    
    return make_response({"task": new_task.to_dict()},201)

@task_db.route("", methods=["GET"])
def get_tasks():
    
    asc_query = request.args.get("title")
    desc_query = request.args.get("desc")
    task_query = Task.query

    if asc_query:
        task_query = Task.query.filter_by(sort=asc_query).order_by(asc(Task.title.upper()))

    # if desc_query:
    #     task_query = Task.query.filter_by(sort=desc_query).order_by(Task.title.desc())

    tasks = task_query.all()
    task_list = [task.to_dict() for task in tasks]
    
    return jsonify(task_list)

@task_db.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()})

@task_db.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()})

@task_db.route("/<task_id>", methods=["DELETE"])
def delete(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task_id} "{task.title}" successfully deleted'})

@task_db.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    request_body = request.get_json()

    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}))








    
        
