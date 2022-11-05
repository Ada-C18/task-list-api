from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app import db
from datetime import datetime
import os
import requests
# import logging
# from slack_logger import SlackHandler, SlackFormatter, SlackLogFilter


task_bp = Blueprint("task", __name__, url_prefix = "/tasks")

# Helper function
def get_task_from_id(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        return abort(make_response({"message" : f"{task_id} is invalid"}, 400))

    chosen_task = Task.query.get(task_id)
   
    if chosen_task is None:
        return abort(make_response({'msg': f' Could not find task item with id : {task_id}'}, 404))
     
    return chosen_task


@task_bp.route('', methods= ['POST'])
def create_one_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body['title'], 
                        description=request_body['description'])
                    # completed_at=request_body['completed_at'])
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task':new_task.to_dict()}), 201


@task_bp.route('', methods=["GET"])
def get_all_tasks():
    query_value = request.args.get("sort") 
    # It's better to check for None rather than check for falsey, in case we are checking for value equal to 0 or False.
    
    if query_value == "asc" :
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif query_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:    
        response.append(task.to_dict())

    return make_response(jsonify(response), 200)


@task_bp.route("/<task_id>", methods= ["GET"])
def get_one_task(task_id):
    
    chosen_task = get_task_from_id(task_id)

    return make_response(jsonify({'task':chosen_task.to_dict()}),200)


@task_bp.route('/<task_id>', methods= ['PUT'])
def update_one_task(task_id):
    update_task= get_task_from_id(task_id)

    request_body = request.get_json()

    try: 
        update_task.title = request_body["title"]
        update_task.description = request_body["description"]
        # update_task.is_complete = request_body["is_complete"]
    except KeyError:
        return jsonify({"msg": "Missing needed data"}), 400
        
    db.session.commit()
    return jsonify({'task':update_task.to_dict()}), 200


@task_bp.route('/<task_id>', methods= ['DELETE'])
def delete_one_task(task_id):
    task_to_delete = get_task_from_id(task_id)

    db.session.delete(task_to_delete)
    db.session.commit()

    return jsonify({
             "details": f'Task {task_to_delete.task_id} "{task_to_delete.title}" successfully deleted'
            }), 200


@task_bp.route('/<task_id>/mark_complete', methods =['PATCH'])
def mark_complete(task_id):
    task= get_task_from_id(task_id)
    task.completed_at = datetime.utcnow()
    db.session.commit()

    path = "https://slack.com/api/chat.postMessage"
    
    headers={"Authorization":os.environ.get("API_KEY")}
    query_params = {
                "channel": "task-notifications",
                "text": f"Someone just completed the task {task.title}"
                }
    requests.post(path, params=query_params, headers=headers)
    
    return jsonify({'task':task.to_dict()}), 200

    
@task_bp.route('/<task_id>/mark_incomplete', methods =['PATCH'])
def mark_incomplete(task_id):
    task= get_task_from_id(task_id)
    task.completed_at = None
  
    db.session.commit()
    return jsonify({'task':task.to_dict()}), 200








