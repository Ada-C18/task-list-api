from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')

@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    # Feel free to add a guard clause
    if "title" not in request_body or "description" not in request_body:
        return make_response("Invalid Request", 400)

    # How we know about Dog
    new_task = Task(
        # You're looking for this key and assign it to name, breed, gender, age
        title=request_body["title"],
        description=request_body["description"],
        #completed_at=request_body["completed_at"]
    )
    # Add this new instance of dog to the database
    db.session.add(new_task)
    db.session.commit()

    # Successful response
    return ({ "task":{
    "id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": bool(new_task.completed_at)
    }},201)

@task_bp.route("", methods=["GET"])
def get_all_tasks():


    tasks = Task.query.all()

    tasks_response = [{"id": task.task_id, "title": task.title, "description": task.description, "is_complete": bool(task.completed_at)}for task in tasks]

    return jsonify(tasks_response), 200


# Path/Endpoint to get a single dog
# Include the id of the record to retrieve as a part of the endpoint
@task_bp.route("/<task_id>", methods=["GET"])
# GET /dog/id
def get_one_task(task_id):
    # Query our db to grab the dog that has the id we want:
    task = Task.query.get(task_id)

    # Send back a single JSON object (dictionary):
    return { "task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }},200
@task_bp.route("/<task_id>", methods=["PUT"])

def edit_task(task_id):
    task = Task.query.get(task_id)
    request_body = request.get_json(task_id)

    task.title = request_body["title"],
    task.description = request_body["description"]

    db.session.commit()

    return make_response({ "task":{
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
    }},200)


@task_bp.route("/<task_id>", methods=["DELETE"])

def delete_task(task_id):
    task = Task.query.get(task_id)
    #request_body = request.get_json(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({f"details": f'Task {task_id} \"{task.title}\" successfully deleted'}),200



