from os import abort
from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request

tasks_bp=Blueprint('tasks_bp',__name__,url_prefix='/tasks')

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"details":f"Invalid data"}, 400))

    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"task {task_id} not found"}, 404))

    return task

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    # handles if title or description not included in post
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details":"Invalid data"},400)

    new_task = Task(title=request_body["title"],
                    description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

    task_response = {"task": new_task.to_dict()}


    return make_response(jsonify(task_response), 201)

# Returns all tasks
@tasks_bp.route("", methods=["GET"])
def return_all_tasks():
    tasks_response = []
    tasks = Task.query.all()


    sort_by_alpha_title_query = request.args.get("sort")

    if sort_by_alpha_title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    if sort_by_alpha_title_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    for task in tasks:
        tasks_response.append(task.to_dict())
    return make_response(jsonify(tasks_response),200)

# Gets one specific task
@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_task(task_id)
    task_response = {"task": task.to_dict()}
    return jsonify(task_response), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_tasks(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()
 
    task_response = {"task": task.to_dict()}


    return make_response(jsonify(task_response), 200)

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)
    task_response = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    db.session.delete(task)
    db.session.commit()
    return jsonify(task_response), 200

# wave 3 
@tasks_bp.route("/<task_id>", methods = ["PATCH"])  
def partial_task_update(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()




