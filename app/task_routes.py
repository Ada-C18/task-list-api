from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from .routes_helper import get_one_obj_or_abort

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    print(request_body)
    if not "title" in request_body or not "description" in request_body:
        return jsonify({"details": "Invalid data"}), 400

    
    new_task = Task(
        title=request_body["title"], # could use dot notation to call instead 
        description=request_body["description"]
        )
    # could do a conditional if completed_at = null in the request, update the task object with is_complete = False

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

@tasks_bp.route("", methods=["GET"])
def get_saved_tasks():
    name_param = request.args.get("name")

    if name_param is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(name=name_param)

    response = [task.to_dict() for task in tasks]

    return jsonify(response), 200


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    
    task_dict = chosen_task.to_dict()
    if not task_dict:
        return jsonify({f"message": "Task with id {task_id} was not found in the database."})
    else:
        return jsonify({"task": task_dict}), 200


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)
    
    request_body = request.get_json()

    if not "title" in request_body or not "description" in request_body:
        return jsonify({"details": "Invalid data"}), 400

    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]

    task_dict = chosen_task.to_dict()

    db.session.commit()

    return jsonify({"task": task_dict}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_obj_or_abort(Task, task_id)

    task_dict = chosen_task.to_dict()

    if not task_dict:
        return jsonify({f"message": "Task with id {task_id} was not found in the database."}), 404
    
    db.session.delete(chosen_task)
    db.session.commit()

    return jsonify({f"details": "Task with id {task_id} {task_dict}['description'] successfully deleted"}), 200
    

    
    
    