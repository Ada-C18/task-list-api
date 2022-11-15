from flask import Blueprint, jsonify, abort, make_response, request
from os import abort
from app.models.task import Task
from app import db
import json
from datetime import datetime
from sqlalchemy import asc, desc

tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")

# now = datetime.now() 
# date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

@tasks_bp.route("", methods=['POST'])
def created_task():
    request_body = request.get_json()
    print(request_body)
    created_task = Task(title=request_body["title"],
                description=request_body["description"])
            # completed_at=request_body["completed_at"])

    if created_task.title == "":
        created_task = Task(details=request_body["details"])
        return created_task
        # make_response({"message":f"Task {created_task.title} invalid"}, 400)

    if created_task.description == "":
        return make_response({"details": "Invalid data"}, 400)
        # return make_response({"message":f"Task {created_task.description} invalid"}, 400)


    # if created_task.completed_at == None:
    #     return make_response({"message":f"Task {created_task.complete_at} invalid"}, 400)

    else:
        db.session.add(created_task)
        db.session.commit()
    
    return jsonify({"task": created_task.build_task_dict()}), 201
    


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
        #     "is_complete": bool(query.completed_at)
        # })

        # for task in query_tasks:
    #         query_lists.append(task.build_task_dict())

    print(query_lists)
   
    


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
    task = validate_task_id(task_id)
    request_body = request.get_json()
    
    task = request_body["task"]
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.is_complete = request_body["completed_at"]

    db.session.commit()

    return make_response( f"Task {task_id} successfully updated", 200)
    # return "task": f"Task {task_id} successfully updated", 200)
    # return make_response("task": f"Task {task_id} successfully updated", 200)


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_tasks(task_id):
    test_task = validate_task_id(task_id)
    result_notice = {"details": f'Task {task_id} "{test_task.title}" successfully deleted'}

    db.session.delete(test_task)
    db.session.commit()

    return make_response(result_notice, 200)

    #     {"details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    # }


