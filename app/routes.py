import datetime
from flask import Blueprint
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from dotenv import load_dotenv
import requests
import os


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model

def validate_request(data):
    try:
        new_task = Task(title =data["title"],
                description =data["description"])
    except:
        abort(make_response(
            {"details": "Invalid data"}, 400))
    return new_task


@task_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = validate_request(request_body)

    db.session.add(new_task)
    db.session.commit()

    return make_response({
            "task": {
            "id":new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }}
    , 201)

@task_bp.route("", methods=["GET"])
def read_all_tasks():

    # get the sort parameter from request
    sort= request.args.get('sort')
    tasks = Task.query.all()

    # reverse is set to a boolean that sort equals "desc" is consider True. If it doesn't equal "desc" it False.
    reverse = sort == "desc"

    def sorting(task):
        return task.title

    tasks.sort(reverse=reverse, key=sorting)

    get_response = []
    for task in tasks:
        get_response.append(dict(
            id=task.task_id,
            title=task.title,
            description=task.description,
            is_complete=bool(task.completed_at)
        ))
        
    return jsonify(get_response)

@task_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):

    task = validate_model(Task,task_id)


    get_response ={
        f"task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete":  bool(task.completed_at)
        }}

    return get_response, 200

    
    

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    update_response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return make_response(update_response), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    task_response =  {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }
    return make_response(task_response), 200

def slack_bot(task):
    url = "https://slack.com/api/chat.postMessage"
    SLACK_API_TOKEN = os.environ.get("SLACK_API_TOKEN")

    data= {"channel":"task-notifications", "text":f"Someone just completed the task {task.title}"}
    headers = {"Authorization": SLACK_API_TOKEN}
    slack = requests.post(url, json=data, headers=headers)
    return slack


@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):

    task = validate_model(Task, task_id)
    
    task.completed_at = datetime.datetime.utcnow()

    slack_bot(task)

    db.session.commit()

    completed_response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return(make_response(completed_response),200)


@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task = validate_model(Task, task_id)
    
    task.completed_at = None

    db.session.commit()

    not_completed_response = {
        "task": {
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }

    return(make_response(not_completed_response),200)


@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = validate_request(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response({
            "goal": {
            "id":new_goal.goal_id,
            "title": new_goal.title,
        }}
    , 201)


@goal_bp.route("", methods=["GET"])
def read_all_goals():

    # get the sort parameter from request
    sort= request.args.get('sort')
    goals = Goal.query.all()

    # reverse is set to a boolean that sort equals "desc" is consider True. If it doesn't equal "desc" it False.
    reverse = sort == "desc"

    def sorting(goals):
        return goal.title

    goals.sort(reverse=reverse, key=sorting)

    get_response = []
    for goal in goals:
        get_response.append(dict(
            id=goal.goal_id,
            title=goal.title,
        ))
        
    return jsonify(get_response)