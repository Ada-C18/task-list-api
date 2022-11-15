import json
from datetime import datetime
from os import abort

from flask import Blueprint, abort, jsonify, make_response, request
from sqlalchemy import asc, desc

from app import db
from app.models.task import Task

tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")

# now = datetime.now() 
# date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

@tasks_bp.route("", methods=['POST'])
def created_task():
    response_body = request.get_json()
  
    if "title" not in response_body or "description" not in response_body:
        return {"details": "Invalid data"}, 400
    
    created_task = Task(title=response_body["title"],
                description=response_body["description"])

    
    db.session.add(created_task)
    db.session.commit()
    
    return jsonify(created_task.build_task_dict()), 201
        # if title is not in response body then return invalid data
        # if description is not in response body then return invalid datay_tasks.description == "":

        # return make_response({"message":f"Task {created_task.description} invalid"}, 400)

  # created_task = Task(title=response_body["title"],
    #             description=response_body["description"],
    #         completed_at=response_body["completed_at"])


    # if created_task.completed_at == None:
    #     return make_response({"message":f"Task {created_task.complete_at} invalid"}, 400)


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} invalid"}, 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response({"message":f"Task {task_id} not found"}, 404))

    return task

@tasks_bp.route('', methods=['GET'])
def query_all():
    
    sort_query = request.args.get("sort")
    
    query_lists = []
    
    if sort_query== "desc":
        query_tasks = Task.query.order_by(Task.title.desc())


    elif sort_query == "asc":
        query_tasks = Task.query.order_by(Task.title.asc())

    else:
        query_tasks = Task.query.all()

    for query in query_tasks:
        query_lists.append(query.build_task_dict())

    return jsonify(query_lists), 200



@tasks_bp.route('/<task_id>', methods=['GET'])
def one_saved_task(task_id):
    task_validate = validate_task_id(task_id)
    
    # task = Task.query.get(task_id)
    if task_id == None:
        return "The task ID submitted, does not exist: error code 404"
    else:    
        return {"task": task_validate.build_task_dict()}
        # query_lists = []
        # for query in task_validate:
        #     query_lists.append(task_validate.build_task_dict())
        # return jsonify(task_validate.build_task_dict())


@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_tasks(task_id):
    
    validate_id = validate_task_id(task_id)

    response_body = request.get_json()
    
    validate_id.title = response_body["title"]
    validate_id.description = response_body["description"]
    # validate_id.completed_at = response_body["completed_at"]

    db.session.commit()

    return jsonify({"task": validate_id.build_task_dict()}),200
    # return "task": f"Task {task_id} successfully updated", 200)
    # return make_response("task": f"Task {task_id} successfully updated", 200)


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_tasks(task_id):
    test_task = validate_task_id(task_id)
    result_notice = {"details": f'Task {task_id} "{test_task.title}" successfully deleted'}

    db.session.delete(test_task)
    db.session.commit()

    return make_response(result_notice, 200)



