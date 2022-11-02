from flask import Blueprint
from flask import Blueprint, jsonify, make_response, request, abort,Response
from app import db
# from app.models import task
from app.models.task import Task
import json

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response(jsonify({"message": "task_id must be an integer"}),400))
    
    matching_task = Task.query.get(task_id)

    if matching_task is None:
        response_str = f"Task with id {task_id} was not found in the database."
        abort(make_response(jsonify({"Message": response_str}), 404))

    return matching_task

@task_bp.route("", methods = ["POST"])
def add_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.task_id} successfully created", 201)

@task_bp.route("", methods=["GET"])
def get_all_tasks():

    title_query = request.args.get("title")
    description_query = request.args.get("description")
    completed_at_query = request.args.get("completed_at")


    if title_query:
        tasks = Task.query.filter_by(title = title_query)
    elif description_query:
        tasks = Task.query.filter_by(description = description_query)
    elif completed_at_query:
        tasks = Task.query.filter_by(completed_At = completed_at_query)
    else:
        tasks = Task.query.all()
    response = []
    for task in tasks:
        if task.completed_at is None:
            task_dict = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
            response.append(task_dict)
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_bike(task_id):
    task = validate_task_id(task_id)
    if task.completed_at is None:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
}
    else:
        task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": True}
    
    return jsonify({"task":task_dict})
    # return json.dumps(task_dict)

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
                return jsonify({"message":"Request must include title, description, and is complete"}),400

    task.title = request_body["title"]
    task.description = request_body["description"]

    task_dict = {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": False}

    db.session.commit()
    return jsonify({"task":task_dict}),200


