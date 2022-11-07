from datetime import datetime
from app import db
from app.models.task import Task
from app.routes.routes_helper import validate_model, validate_input_data, error_message
from flask import Blueprint, jsonify, make_response, request, abort

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')


# create a task (POST)
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    new_task = validate_input_data(Task, request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201

# read one task (GET)
@tasks_bp.route("/<id>", methods=["GET"])
def read_one_task(id):
    task = validate_model(Task, id)

    return jsonify({"task": task.to_dict()}), 200
    
# read all tasks (GET)
@tasks_bp.route("", methods=["GET"])
def read_all_tasks():

    sort_asc_query = request.args.get("sort")

    if sort_asc_query == "asc": 
        tasks = Task.query.order_by(Task.title)
    elif sort_asc_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response)


# replace a task (PUT)
@tasks_bp.route("/<id>", methods=["PUT"])
def update_task(id):
    task = validate_model(Task, id)

    request_body = request.get_json()

    task.update(request_body)

    db.session.commit()
    
    response = {"task": task.to_dict()}
    return response


# update a task (PATCH)
@tasks_bp.route("/<id>/mark_complete", methods=["PATCH"])
def mark_complete_task(id):
    task = validate_model(Task, id)

    task.completed_at = datetime.utcnow()

    db.session.commit()
   
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<id>/mark_incomplete", methods=["PATCH"])
def mark_incomple_task(id):
    task = validate_model(Task, id)

    task.completed_at = None

    db.session.commit()
   
    return jsonify({"task": task.to_dict()}), 200


# delete a task (DELETE)
@tasks_bp.route("/<id>", methods=["DELETE"])
def delete_task(id):
    task = validate_model(Task, id)
    title = str(task.title )
    db.session.delete(task)
    db.session.commit()

    # Returns error 
    return(make_response({"details": f"Task {id} \"{title}\" successfully deleted"}), 200)


