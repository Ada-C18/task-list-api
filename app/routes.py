from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model


@task_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                    description=request_body["description"])
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    return make_response({"task":{
            "id": new_task.task_id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }}, 201)

@task_bp.route("", methods=["GET"])
def read_all_tasks():

    sort_query = request.args.get("sort")

    if sort_query == "asc":
        task = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        task = Task.query.order_by(Task.title.desc())
    else:
        task = Task.query.all()

    task_response = []
    for task in task:
        task_response.append(task.to_dict())
        
    return jsonify(task_response)

@task_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return make_response({"task": task.to_dict()})
 
def slack_bot_message(message):
    PATH = "https://slack.com/api/chat.postMessage"
    SLACK_API_KEY = os.environ.get("SLACK_API_KEY")

    query_params = {
        "channel" : "#task-notification",
        "text" : message
    }

    requests.post(PATH, params=query_params,headers={"Authorization": SLACK_API_KEY})

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def complete_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    
    db.session.commit()

    slack_bot_message(f"Someone just completed the task {task.title}")

    return make_response({"task": task.to_dict()})

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_complete_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return make_response({"task": task.to_dict()})
        

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details":f'Task {task_id} "{task.title}" successfully deleted'})

################## GOAL ROUTES ######################


@goal_bp.route("", methods=["POST"])
def handle_goals():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response({"goal":{
            "id": new_goal.goal_id,
            "title": new_goal.title
        }}, 201)

@goal_bp.route("", methods=["GET"])
def read_all_goals():

    goal = Goal.query.all()
    goal_response = []
    for goal in goal:
        goal_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })

    return jsonify(goal_response)

@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal":{
            "id": goal.goal_id,
            "title": goal.title,
        }}

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response({"goal":{
            "id": goal.goal_id,
            "title": goal.title
        }})

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f'Goal {goal_id} "{goal.title}" successfully deleted'})

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_task_ids_to_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.tasks = [Task.query.get(task_id) for task_id in request_body["task_ids"]]

    db.session.commit()

    return {"id":goal.goal_id,
            "task_ids":[task.task_id for task in goal.tasks]}, 200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])

def read_tasks(goal_id):

    goal = validate_model(Goal, goal_id)

    tasks_response = []
    for task in goal.tasks:
        tasks_response.append(task.to_dict())

    return make_response({
            "id": goal.goal_id,
            "title": goal.title,
            "tasks": tasks_response
        })
