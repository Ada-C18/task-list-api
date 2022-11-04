from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')

def validate_task(id):
    try:
        id = int(id)
    except:
        abort(make_response({"message": f"task {id} invalid"}, 400))

    task = Task.query.get(id)
    if not task:
        abort(make_response({"message": f"task {id} not found"}, 404))
    return task

# ---------------------------------
# create a task (POST)
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"])

    db.session.add(new_task)
    db.session.commit()

   
    return make_response({"task": new_task.to_dict()}, 201)

# ---------------------------------
# read one task (GET)
@tasks_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_task(id)

    response = {"task": task.to_dict()}
    return response

# ---------------------------------
# read all tasks (GET)
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    tasks_response = []
    tasks = Task.query.all()
    tasks_response = [task.to_dict() for task in tasks]
    
    return jsonify(tasks_response)

# ---------------------------------
# replace a task (PUT)
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_task(id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()
    
    response = {"task": task.to_dict()}
    return response


# update a task (PATCH)
# not required- might not be correct, but hopefully helps CRUD
@tasks_bp.route("/<id>", methods=["PATCH"])
def patch_task(id):
    task = validate_task(id)

    request_body = request.get_json()

    try:
        task.title = request_body["title"]
    except: 
        pass

    try: 
        task.description = request_body["description"]
    except: 
        pass

    try:
        task.completed_at = request_body["completed_at"]
    except:
        pass

    db.session.commit()
    return make_response(f"task {task.title} successfully updated", 201)


# delete a task (DELETE)
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_task(id)

    db.session.delete(task)
    db.session.commit()

    response = make_response(f"details: Task {task.id} {task.description} successfully deleted", 202)
    return response

