
from app import db
from datetime import date
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
import requests, os

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#Helper function:
def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task_id: `{task_id}`. ID must be an integer"
        abort(make_response(jsonify({"message":response_str}), 400))
    
    matching_task = Task.query.get(task_id)

    if not matching_task:
        response_str = f"Task with id `{task_id}` was not found in the database."
        abort(make_response(jsonify({"message":response_str}), 404))
    
    return matching_task

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@task_bp.route("", methods=["POST"])
def add_task():
    
    request_body = request.get_json()
    
    if "title" not in request_body or \
        "description" not in request_body:
            # or \
        # "complete_at" not in request_body:
        return jsonify({"details":"Invalid data"}), 400

    new_task = Task (
        title=request_body["title"],
        description=request_body["description"],
        # completed_at=request_body.get("completed_at"),
        # completed_at=request_body["completed_at"],
        completed_at = None
        # is_complete=request_body.get("is_complete")
    )
    db.session.add(new_task)
    db.session.commit()

    # return make_response (f"Task '{new_task.to_dict()})' successfully created", 201)
    return jsonify({"task": new_task.to_dict()}), 201
    # return jsonify({"task_id": new_task.task_id}), 201
    
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@task_bp.route("", methods=["GET"])
def get_all_tasks():
    
    name_param = request.args.get("sort")  #KEY for the KEY value pair

    if name_param == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif name_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    
    response = []
    for task in tasks:
        response.append(task.to_dict())
    return jsonify(response), 200

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@task_bp.route("<task_id>", methods=["GET"])
def get_one_task(task_id):
    
    selected_task = get_one_task_or_abort(task_id)
    
    return jsonify({"task" : selected_task.to_dict()}), 200

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):

    selected_task= get_one_task_or_abort(task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"message":"Request must include title, description."}), 400

    selected_task.title = request_body["title"]
    selected_task.description = request_body["description"]

    db.session.commit()

    # return jsonify({f"task": f"Successfully replaced bike with id `{bike_id}`"}), 200
    return jsonify({"task" : selected_task.to_dict()}), 200


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    selected_task= get_one_task_or_abort(task_id)
    
    db.session.delete(selected_task)
    db.session.commit()

    return jsonify({"details": f'Task {task_id} "{selected_task.title}" successfully deleted'}), 200

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>ok<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_incompleted_task_to_completed(task_id):

    selected_task= get_one_task_or_abort(task_id)
    # request_body = request.get_json()

    selected_task.completed_at = date.today()
    
    db.session.commit()

    requests.post("https://slack.com/api/chat.postMessage", data={"channel":"task-notifications", "text":"Someone just completed the task My Beautiful Task"}, headers={"authorization":os.environ.get("SLACK_TOKEN")})
    
    # return jsonify({f"task": f"Successfully replaced bike with id `{bike_id}`"}), 200
    return jsonify({"task" : selected_task.to_dict()}), 200


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>OK<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_completed_task_to_incompleted(task_id):

    selected_task=get_one_task_or_abort(task_id)
    # request_body = request.get_json()

    selected_task.completed_at = None    
    db.session.commit()
    
    # return jsonify({f"task": f"Successfully replaced bike with id `{bike_id}`"}), 200
    return jsonify({"task" : selected_task.to_dict()}), 200

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<