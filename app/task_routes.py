from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from datetime import datetime
import os


task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

#---------------------------------------GET------------------------------------------------

def get_one_task_or_abort(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response_str = f"Invalid task ID: {task_id}. ID must be an integer."
        abort(make_response(jsonify({"Message":response_str}), 400))
    
    matching_task = Task.query.get(task_id)

    if not matching_task:
        response_str = f"Task with id #{task_id} was not found in the database."
        abort(make_response(jsonify({"Message": response_str}), 404))

    return matching_task

@task_bp.route("", methods=["GET"])
def read_all_tasks():
    
    sort_param = request.args.get("sort")
    if sort_param == "asc":        
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_param is None:
        tasks = Task.query.all()
    elif sort_param == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    response = []
    for task in tasks:
        task_dict = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
        response.append(task_dict)
    return jsonify(response), 200
    
    
    name_param = request.args.get("title")

    if name_param is None:
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(title=name_param)
    
    response = []

    for task in tasks:
        if task.completed_at is None:
            task_dict = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": False
            }
            response.append(task_dict)
        else:
            task_dict = {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "completed at": task.completed_at,
                "is_complete": True}
            response.append(task_dict)
    return jsonify(response), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)

    # if chosen_task.completed_at is None:
    #     task = {
    #         "id": chosen_task.task_id,
    #         "title": chosen_task.title,
    #         "description": chosen_task.description,
    #         "is_complete": False
    #     }

    # else:
    #     task = {
    #         "id": chosen_task.task_id,
    #         "title": chosen_task.title,
    #         "description": chosen_task.description,
    #         "completed at": chosen_task.completed_at,
    #         "is_complete": True}
        
    return jsonify({"task": chosen_task.to_dict()}), 200




#-------------------------------------POST------------------------------------------------
@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    
    if "title" not in request_body or \
        "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(title = request_body["title"], description = request_body["description"])
    

    db.session.add(new_task)
    db.session.commit()


    return jsonify({"task": new_task.to_dict()}), 201

#---------------------------------------UPDATE------------------------------------------------
@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)

    request_body = request.get_json()

    if "title" not in request_body or \
        "description" not in request_body:
            return jsonify({"Message":"Request must include title and description"})
    
    chosen_task.title = request_body["title"]
    chosen_task.description = request_body["description"]
    
    db.session.commit()

    return jsonify({"task": chosen_task.to_dict()}), 200

#---------------------------------------DELETE------------------------------------------------
@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)

    db.session.delete(chosen_task)
    db.session.commit()
    return jsonify({"details": f'Task {task_id} "{chosen_task.title}" successfully deleted'}), 200


#---------------------------------------PATCH------------------------------------------------
@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incompleted_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    today = datetime.now()
    
    if chosen_task.completed_at is None:
        chosen_task.completed_at = today
        chosen_task.is_complete = True

    else:
        chosen_task.completed_at = today
        chosen_task.is_complete = True
    db.session.commit()
    
    header = os.environ.get("api_slack")
    url = "http://slack.com/api/chat.postMessage"
    response_str = f"Someone just completed the task {chosen_task.title}"
    data = {"channel":"task-notifications", "text": response_str}
    r = requests.post(url, params=data, headers={"Authorization":header})


    return jsonify({"task": chosen_task.to_dict()}), 200

    

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_on_completed_task(task_id):
    chosen_task = get_one_task_or_abort(task_id)
    today = datetime.now()
    
    if chosen_task.completed_at:
        chosen_task.completed_at = None
        chosen_task.is_complete = None
    else:
        chosen_task.completed_at = None
        chosen_task.is_complete = None

    db.session.commit()
    return jsonify({"task": chosen_task.to_dict()}), 200

