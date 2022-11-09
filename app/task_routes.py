from app.models.task import Task
from app.helper_functions import *
from app import db
from flask import Blueprint, request, make_response, jsonify, abort
from datetime import date
import requests
import os
from dotenv import load_dotenv

# Functions are grouped by endpoint, method routing logic (eg GET vs POST) is handled within the function
# I consider this to be DRYer and more RESTful

load_dotenv()

# Blueprints
tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

# Routes

# Tasks Endpoint
@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():

    if request.method == "POST":
        task = Task.from_dict(request.get_json())
        
        if task == False:
            return make_response({"details": "Invalid data"}, 400)
        
        db.session.add(task)
        db.session.commit()

        db.session.refresh(task)
        task = task.to_dict()
        response = {"task":task}
        return make_response(response,201)

    elif request.method == "GET":
        sort = request.args.get("sort")
        if sort == "asc":
            tasks = Task.query.order_by(Task.title.asc()).all()
        elif sort == "desc":
            tasks = Task.query.order_by(Task.title.desc()).all()
        
        else:
            tasks = Task.query.all()
        response_body = [task.to_dict() for task in tasks]
        return make_response(jsonify(response_body), 200)

# Individual Task Endpoints
@tasks_bp.route("/<id>", methods=["GET","DELETE","PUT"])
def handle_individual_task(id):
    task = validate_id(Task, id)
    
    if request.method == "GET":
        return make_response({"task":task.to_dict()}, 200)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)
    
    elif request.method == "PUT":
        new_task = request.get_json()
        task.description = new_task["description"]
        task.title = new_task["title"]
        db.session.commit()
        return make_response({"task":task.to_dict()}, 200)

@tasks_bp.route("/<id>/<mark>", methods=["PATCH"])
def mark_task(id, mark):
    task = validate_id(Task, id)
    mark = mark_truthy_falsy(mark)
    if mark == True:
        if task.completed_at == None:
            # connect to Slack API to send a message to the task-notifications channel
            SLACK_URL = "https://slack.com/api/chat.postMessage"
            PARAMS = {"channel":"task-notifications",
                     "text":f"Someone just completed the task {task.to_dict()['title']}"
                     }
            HEADERS ={"Authorization": f"Bearer {os.environ.get('SLACK_BOT_TOKEN')}"}
            requests.post(url = SLACK_URL, headers=HEADERS, params=PARAMS,)
        task.completed_at = date.today()
        db.session.commit()
        return make_response({"task":task.to_dict()},200)
    elif mark == False:
        task.completed_at = None
        db.session.commit()
        return make_response({"task":task.to_dict()},200)
