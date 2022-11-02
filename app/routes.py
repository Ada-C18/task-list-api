from flask import Blueprint, request, jsonify, make_response, abort
from app import db 
from app.models.task import Task 

task_list_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

#GET all tasks
@task_list_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    response = []
    for task in tasks:
        response.append(task.to_dict())

    return jsonify(response), 200


# @task_list_bp.route("/<task_id>", methods= ["GET"])
# def get_one_task(task_id):
#     task = Task.query.get(task_id)
#     if not task:
#         abort(make_response({"message": f"task {task_id} not found"}, 404))
#     else:
#         response = {"task": task.to_dict()}
#         return jsonify(response), 200

#GET one task
@task_list_bp.route("/<task_id>", methods= ["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)
    response = {"task": task.to_dict()}
    return jsonify(response), 200

#CREATE new task
@task_list_bp.route("", methods = ["POST"])
def create_new_task():
    request_body = request.get_json()
    new_task = Task(
        title = request_body["title"],
        description = request_body["description"],
    )
    
    db.session.add(new_task)
    db.session.commit()

    response_body = {"task": new_task.to_dict()}
    return jsonify(response_body), 201


#UPDATE task
@task_list_bp.route("/<task_id>", methods = ["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    response_body = {"task": task.to_dict()}

    return jsonify(response_body)

#DELETE task
@task_list_bp.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{task.title}" successfully deleted'}), 200 

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task