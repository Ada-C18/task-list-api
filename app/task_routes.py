from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from app import db
import os
import requests




tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    try:
        request_body["title"]
    except:
        abort(make_response({"details":"Invalid data"}, 400))
    try:
        request_body["description"]
    except:
        abort(make_response({"details":"Invalid data"}, 400))

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"]
        )

    db.session.add(new_task)
    db.session.commit()

    response = {
            "task": new_task.to_dict()
            }
    return jsonify(response), 201


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks_response = []
    sort_query = request.args.get("sort")

    if sort_query:
        if sort_query == 'desc':
            tasks = Task.query.order_by(Task.title.desc())
        else:
            tasks = Task.query.order_by(Task.title).all()
    else:
        tasks = Task.query.all()

    for task in tasks:
        tasks_response.append({
            "id":task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.is_complete)
        })

    return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_task(task_id)

    response = {
        "task": task.to_dict()
    }
    if task.goal_id == None:
        pass
    else:
        response["task"]["goal_id"] = task.goal_id
    
    return response

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except: 
        abort(make_response({"message":f"task {task_id} invalid"}, 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": "id number not found"}, 404))
    
    return task

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    response = {
        "task": task.to_dict()
    }

    return jsonify(response)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete_on_incomplete_task(task_id):
    task = validate_task(task_id)
    task.mark_complete()
    db.session.commit()

    URL = "https://slack.com/api/chat.postMessage"
    payload={"channel":"slack-bot-test-channel",
    "text": f"Someone just completed the task {task.title}"}
    headers = {
    "Authorization": os.environ.get('SLACK_TOKEN')
    }
    requests.post(URL, data=payload, headers=headers)
    
    response = {
        "task": task.to_dict()
    }
    return jsonify(response)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_oncomplete_task(task_id):
    task = validate_task(task_id)

    task.mark_incomplete()
    db.session.commit()

    response = {
        "task": task.to_dict()
    }
    return jsonify(response)