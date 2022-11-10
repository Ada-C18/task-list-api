from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from datetime import date

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


#Validate
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message" : f"Task ID '{task_id}' invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message" : f"Task ID '{task_id}' not found"}, 404))
    
    return task

#CREATE a task
@tasks_bp.route("", methods=['POST'])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(title=request_body["title"], 
                description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

#READ all tasks
@tasks_bp.route("", methods=['GET'])
def get_all_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    task_response = []
    for task in tasks:
        task_response.append(task.to_dict())

    return jsonify(task_response)


#READ one task
@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()})

#UPDATE one task
@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id): 
    task = validate_task(task_id)
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()})


#UPDATE mark task complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = date.today()

    db.session.commit()

    return make_response({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task(task_id)

    task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_dict()}), 200


#DELETE one task
@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):    
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200