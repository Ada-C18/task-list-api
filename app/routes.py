from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from app import db

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_tasks():
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"])
                        # completed_at=request_body["is_complete"])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return make_response(jsonify({"task": new_task.to_dict()}), 201)

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    title_query = request.args.get("title")
    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    
    return jsonify(tasks_response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task_id(task_id)

    return make_response(jsonify({"task": task.to_dict()})), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task_id(task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    # task.is_complete = request_body["completed_at"]

    db.session.commit()

    return make_response(jsonify({"task": task.to_dict()}), 200)

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response(jsonify({"details": f"Task {task_id} \"{task.title}\" successfully deleted"}), 200)

#helper function
def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))
    
    return task
