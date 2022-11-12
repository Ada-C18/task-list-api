from flask import Blueprint, jsonify, abort, make_response, request
from os import abort
from app.models.task import Task
from app import db
import json
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")

now = datetime.now() 
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")


@tasks_bp.route("", methods=['POST'])
def created_task():
    request_body = request.get_json()
    print(request_body)
    created_task = Task(title=request_body["title"],
                description=request_body["description"],
            completed_at=request_body["completed_at"])
    
    if created_task.title == "":
        return abort(make_response({"message":f"Task {created_task.title} invalid"}, 400))

    elif created_task.description == "":
        return abort(make_response({"message":f"Task {created_task.description} invalid"}, 400))


    elif created_task.completed_at == "":
        return abort(make_response({"message":f"Task {created_task.completed_at} invalid"}, 400))

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
    all_tasks = Task.query.all()
    tasks_lists = []
    for task in all_tasks:
            tasks_lists.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "completed_at": bool(task.completed_at)
            })
    print(tasks_lists)
    return jsonify(tasks_lists)

@tasks_bp.route('/<task_id>', methods=['GET'])
def one_saved_task(task_id):
    # task_validate = validate_task_id(task_id)
    task = Task.query.get(task_id)
    if task == None:
        return "The task ID submitted, does not exist: error code 404"
    else:      
        return {
            "id": task.task_id,
            "title": task.title,
            "description": task.description
        }


@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_tasks(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response(f"Task {task_id} successfully updated", 200)


@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_tasks(task_id):
    test_task = validate_task_id(task_id)

    db.session.delete(test_task)
    db.session.commit()

    return make_response(f"Task #{task_id} successfully deleted, 200 OK")


