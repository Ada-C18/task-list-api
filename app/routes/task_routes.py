from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.task import Task
from sqlalchemy import asc,desc
from datetime import date
import os
import slack
from pathlib import Path
from dotenv import load_dotenv
import requests
import json
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)
# client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

def post_message_to_slack(task_id):
    task = Task.query.get(task_id)
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': os.environ.get("SLACK_TOKEN"),
        'channel': "C049FQLJTBN",
        'text': f"Someone just completed the task {task.title}"}).json()
    

task_bp = Blueprint('task_bp', __name__, url_prefix='/tasks')


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return make_response({"details":"Invalid data"}), 400

    new_task = Task(
    
        title=request_body["title"],
        description=request_body["description"],
        #completed_at=request_body["completed_at"]
    )
    
    db.session.add(new_task)
    db.session.commit()

    return ({ "task":{
    "id": new_task.task_id,
    "title": new_task.title,
    "description": new_task.description,
    "is_complete": bool(new_task.completed_at)
    }},201)



@task_bp.route("", methods=["GET"])
def get_all_tasks():

    title_query = request.args.get("sort")

    if title_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif title_query == "desc":
        tasks = Task.query.order_by(desc(Task.title))
    else:
        tasks = Task.query.all()

    tasks_response = [Task.to_dict(task)for task in tasks]

    return jsonify(tasks_response), 200



@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    
    task = Task.query.get(task_id)
    if not task:
        return make_response({"details":"Id not found"}), 404

    return make_response({ "task":
        Task.to_dict(task)
    })



@task_bp.route("/<task_id>", methods=["PUT"])
def edit_task(task_id):

    task = Task.query.get(task_id)

    if not task:
        return make_response({"details":"Id not found"}), 404
    request_body = request.get_json(task_id)

    task.title = request_body["title"],
    task.description = request_body["description"]

    db.session.commit()

    return make_response({ "task":
        Task.to_dict(task)
    })

    


@task_bp.route("/<task_id>", methods=["DELETE"])

def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return make_response({"details":"Id not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return make_response({f"details": f'Task {task_id} \"{task.title}\" successfully deleted'}),200


@task_bp.route("/<task_id>/<complete>", methods=["PATCH"])
def patch_task_complete(task_id, complete):

    task = Task.query.get(task_id)

    if not task:
        return make_response({"details":"Id not found"}), 404 

    if complete == "mark_complete":
        task.completed_at = date.today()
        post_message_to_slack(task_id)
        # client.chat_postMessage(channel='#slack-bot-test-channel',text=f"Someone just completed the task {task.title}")

    elif complete == "mark_incomplete":
        task.completed_at = None

    db.session.commit()

    return make_response({ "task":
        Task.to_dict(task)
    })
