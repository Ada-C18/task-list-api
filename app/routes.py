from app import db
from .models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message" : f"task id: {task_id} is invalid"}, 400))
    
    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message" : f"task {task_id} not found"}, 404))
    
    return task


@task_bp.route("", methods=["GET"])
def get_all_task():
    response = []
    task_list = Task.query.all()
    for task in task_list:
        response.append(task.to_dict())
    return jsonify(response), 200


    

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()

    new_task = Task (title = request_body["title"],
        description = request_body["description"]) 

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task" : new_task.to_dict()}, 201)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id): 
    
    task = validate_task(task_id)
    
    return {"task" : task.to_dict()}, 200

@task_bp.route ("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task" : task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()
    
    return make_response({"details" : f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)


