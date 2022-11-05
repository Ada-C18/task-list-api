from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from sqlalchemy import text
from app import db
import datetime

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

    if not "title" in request_body or not "description" in request_body:
            abort(make_response({"details": "Invalid data"}, 400))
    
    new_task = Task(description=request_body["description"],
        title=request_body["title"]
        )

    db.session.add(new_task)
    db.session.commit()
    
    return make_response({"task": new_task.to_dict()},201)

@task_db.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()})

@task_db.route("", methods=["GET"])
def get_tasks():
    
    sort_query = request.args.get("sort")
    task_query = Task.query

    if sort_query:
        if "asc" in sort_query:
            task_query = task_query.order_by(text('title asc'))
        elif "desc" in sort_query:
            task_query = Task.query.order_by(text('title desc'))

    tasks = task_query.all()

    task_list = [task.to_dict() for task in tasks]
    
    return jsonify(task_list)

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
def mark_complete(task_id) :
    task_id = validate_task(task_id)

    task_id.completed_at = datetime.datetime.now()

    db.session.commit()

    return make_response({"task": task_id.to_dict()})

@task_db.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task_id = validate_task(task_id)

    task_id.completed_at = None

    db.session.commit()

    return make_response({"task": task_id.to_dict()})







    
        
