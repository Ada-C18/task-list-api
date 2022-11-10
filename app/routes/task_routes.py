import os
from app import db
import requests
from datetime import date
from app.models.task import Task
from app.routes.routes_helpers import *
from flask import Blueprint, jsonify, make_response, request

tasks_bp = Blueprint('tasks_bp', __name__, url_prefix='/tasks')
root_bp = Blueprint("root_bp", __name__)

SLACK_API_URL = "https://slack.com/api/chat.postMessage"
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

# Home page
@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Ghameerah's Task List API",
        "message": "Fun with Flask",
    }

# Index
@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    # Get all tasks
    if request.method == "GET":
        task_query = Task.query

        sort = request.args.get("sort")
        if sort == "desc":
            task_query = task_query.order_by(Task.title.desc())
        elif sort == "asc":
            task_query = task_query.order_by(Task.title.asc())

        tasks = task_query.all()
        tasks_response = [task.to_json() for task in tasks]

        return jsonify(tasks_response), 200

    # Create a new task
    elif request.method == "POST":
        request_body = request.get_json()

        try:
            new_task = Task.from_dict(request_body)
        except KeyError:
            return (f"Invalid data", 400)

        # Add this new instance of task to the database
        db.session.add(new_task)
        db.session.commit()

        # Successful response
        return {
            "task": new_task.to_json()
        }, 201

# Path/Endpoint to get a single task
# Include the id of the record to retrieve as a part of the endpoint
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])

# GET /task/id
def handle_task(task_id):
    # Query our db to grab the task that has the id we want:
    task = Task.query.get(task_id)

    # Show a single task
    if request.method == "GET":
        return task.to_json(), 200
    
    # Update a task
    elif request.method == "PUT":
        request_body = request.get_json()

        task.update(request_body)

        # Update this task in the database
        db.session.commit()

        # Successful response
        return {
            "task": task.to_json()
        }, 200

    # Delete a task
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()

    return {
        "details": f'Task {task.task_id} \"{task.title}\" successfully deleted',
    }, 202

# PATCH /task/id/mark_complete
@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])

def mark_complete_task(task_id):
    task = get_record_by_id(Task, task_id)
    task.completed_at = date.today()

    print(task)
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
    }
    
    if task.completed_at:
        data = {
            "channel": "task-notifications",
            "text": f"Task {task.title} has been marked complete",
        }
    else:
        data = {
            "channel": "task-notifications",
            "text": f"Task {task.title} has been marked incomplete",
        }
    
    requests.post(SLACK_API_URL, headers=headers, data=data)

    db.session.commit()

    return task.to_json(), 200


# PATCH /task/id/mark_incomplete
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete_task(task_id):
    task = get_record_by_id(Task, task_id)
    task.completed_at = None

    db.session.commit()

    return task.to_json(), 200
