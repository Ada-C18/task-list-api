from flask import Blueprint, request, jsonify, make_response, abort
from app import db 
from app.models.task import Task 

task_list_bp = Blueprint("tasks", __name__, url_prefix = "/tasks")

#GET all tasks 
@task_list_bp.route("", methods=["GET"])
def get_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query:
        tasks = get_tasks_sorted(sort_query)
    else:
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
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
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

#PATCH complete task
# @task_list_bp.route("/<task_id>/mark_complete", methods = ["PATCH"])
# def mark_complete(task_id):
#     complete_query = 

#================== Helper Functions=================
def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message": f"task {task_id} not found"}, 404))

    return task

#GET sorted tasks helper function
def get_tasks_sorted(sort_query):
    if sort_query == "desc": 
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.order_by(Task.title).all()

    return(tasks)