from flask import Blueprint, jsonify, request, make_response, abort
from app import db
from app.models.task import Task

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#--------------------------------helper functions---------------------------
def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: '{task_id}'. ID must be an integer"
        abort(make_response(jsonify({"message": response_str}), 404))

    matching_task = Task.query.get(task_id)

    if not matching_task:
        response_str = f"Task with ID '{task_id}' was not found in the database"
        abort(make_response(jsonify({"message":response_str}), 404))

    return matching_task

#---------------------------POST-------------------------------------------- 
@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    if "title" not in request_body or\
        "description" not in request_body:
            return jsonify({"details": "Invalid data"}), 400

    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
        #completed_at = request_body["completed_at"]
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.create_dict()}), 201 


#--------------------------------------GET------------------------------------
@task_bp.route("", methods=["GET"])
def get_all_tasks():

    tasks =  Task.query.all()

    response = []
    for task in tasks:
        response.append(task.create_dict())
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):

    task = get_one_task_or_abort(task_id)

    return jsonify({"task": task.create_dict()}), 200

#--------------------------------PUT-------------------------
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_values(task_id):
    task = get_one_task_or_abort(task_id)
    request_body = request.get_json()

    if "title" not in request_body or\
        "description" not in request_body:
            return jsonify({"details": "Invalid data"})

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return jsonify({"task": task.create_dict()}), 200

#-------------------------DELETE----------------------------
@task_bp.route("/<task_id>", methods=["DELETE"])
def detlete_one_task(task_id):
    task = get_one_task_or_abort(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200