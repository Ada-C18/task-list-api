from app import db
from .models.task import Task
from flask import Blueprint, request, make_response, jsonify, abort
import sqlalchemy 
import datetime


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


# all task methods
    # Create
@task_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()
    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task" : new_task.to_dict()}, 201)
    
    # Read
@task_bp.route("", methods=["GET"])
def get_all_task():
    
    sort_query = request.args.get("sort")
    if sort_query:
        sort_function = getattr(sqlalchemy, sort_query)
        task_list = Task.query.order_by(sort_function(Task.title))
    else:
        task_list = Task.query.all()
    
    response = []    
    for task in task_list:
        response.append(task.to_dict())
    
    return jsonify(response), 200  



# Individual task methods

    # Read
@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id): 
    
    task = Task.validate_task_id(task_id)
    
    return {"task" : task.to_dict()}, 200

    # Update
@task_bp.route ("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.validate_task_id(task_id)
    
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task" : task.to_dict()}, 200

@task_bp.route("<task_id>/<marker>", methods=["PATCH"])
def mark_task_status(task_id, marker):
    task = Task.validate_task_id(task_id)
    eval("task." + marker + "()")
    

    db.session.commit()

    return {"task" : task.to_dict()}, 200
    

    



    # Delete
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()
    
    return make_response({"details" : f"Task {task_id} \"{task.title}\" successfully deleted"}, 200)


