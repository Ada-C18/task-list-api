from flask import Blueprint
from flask import Blueprint, jsonify, make_response, request, abort,Response
from app import db
from app.models.task import Task
from sqlalchemy import asc, desc
import datetime


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify({"message": "task_id must be an integer"}),400))
    
    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Task with id {task_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return matching_task

@task_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()
    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({"details": "Invalid data"}),400

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    task_dict = new_task.to_dict()

    return jsonify({"task":task_dict}),201

@task_bp.route("", methods=["GET"])
def get_all_tasks():

    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_at")
    sort_at_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title = title_query)
    elif description_query:
        tasks = Task.query.filter_by(description = description_query)
    elif completed_at_query:
        tasks = Task.query.filter_by(completed_At = completed_at_query)
    elif sort_at_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_at_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append(task.to_dict())
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task_id(task_id)
    task_dict = task.to_dict()
    
    return jsonify({"task":task_dict})

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
                return jsonify({"message":"Request must include title, description, and is complete"}),400

    task.title = request_body["title"]
    task.description = request_body["description"]

    task_dict = task.to_dict()

    db.session.commit()
    return jsonify({"task":task_dict}),200

@task_bp.route("/<task_id>",methods = ['DELETE'])
def delete_task(task_id):
    task = validate_task_id(task_id)
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details":f"Task {task.task_id} \"{task.title}\" successfully deleted"}),200

@task_bp.route("/<task_id>/mark_complete",methods = ['PATCH'])
def mark_complete_on_incomplete_task(task_id):
    task = validate_task_id(task_id)

    datetime_object = datetime.datetime.now()
    task.completed_at = datetime_object
    task.is_complete = True
    task_dict = task.to_dict()
    
    db.session.commit()

    return jsonify({"task":task_dict})

@task_bp.route("/<task_id>/mark_incomplete",methods = ['PATCH'])
def mark_incomplete_on_complete_task(task_id):
    task = validate_task_id(task_id)

    task.completed_at = None
    task.is_complete = False
    task_dict = task.to_dict()
    
    db.session.commit()

    return jsonify({"task":task_dict})


