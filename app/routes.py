from flask import Blueprint, jsonify, request, make_response, abort
from app.models.task import Task
from sqlalchemy import desc, asc
import datetime
import requests
import os
from app import db

def slackbot_call(message):
    PATH = "https://slack.com/api/chat.postMessage"
    parameters = {
        "channel": "task-notifications",
        "text": message
    }

    requests.post(
        PATH, 
        params=parameters, 
        headers={"Authorization": os.environ.get("SLACKBOT_API_KEY")}
    )

def validate_model_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response(
            f"{model_id} is an invalid input. Please input an integer.", 400
                )
            )
    
    model = cls.query.get(model_id)
    if model:
        return model
    else:
        abort(make_response({"error": f"Item #{model_id} cannot be found"}, 404))
        


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET"])
def retrieve_tasks():
    tasks = Task.query.all()
    tasks_response = []
    sort_query = request.args.get("sort")

    if sort_query == "asc":
        tasks = Task.query.order_by(asc("title"))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc("title"))

    for task in tasks:
        tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": (task.completed_at == True)
            })

    if sort_query == "asc":
        tasks = Task.query.order_by(asc("title"))
    elif sort_query == "desc":
        tasks = Task.query.order_by(desc("title"))
    return jsonify(tasks_response)

@tasks_bp.route("", methods = ["POST"])
def create_task():
    request_body = request.get_json()

    if not request_body.get("title") or not request_body.get("description"):
        return {"details": "Invalid data"}, 400
    
    new_task = Task(
        title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body.get("completed_at")
        )
    db.session.add(new_task)
    db.session.commit()
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": (new_task.completed_at == True)
        }
    }, 201

@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = validate_model_id(Task, task_id)
    if task.goal_id:
        return {"task": {
            "id": task.task_id,
            "goal_id": task.goal_id,
            "title": task.title,
            "description": task.description,
            "is_complete": (task.completed_at == True)
            }
        }
    else:
        return {"task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": (task.completed_at == True)
            }
        }

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model_id(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")

    db.session.commit()

    return make_response({
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": (task.completed_at == True)
            }
        })

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
        })

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def update_task_as_complete(task_id):
    task = validate_model_id(Task, task_id)
    task.completed_at = datetime.datetime.now()
    db.session.commit()

    slackbot_call(f"Someone just completed the task {task.title}")

    return make_response({
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": (bool(task.completed_at))
            }
        })



@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def update_task_as_incomplete(task_id):
    task = validate_model_id(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response({
        "task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": (bool(task.completed_at))
            }
        })
