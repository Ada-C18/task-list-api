from flask import Blueprint, jsonify, make_response, abort, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

SLACK_BOT_API_URL = "https://slack.com/api/chat.postMessage"
load_dotenv()
slack_auth_key = os.environ.get("SLACK_BOT_API_KEY")

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(jsonify({"message":f"{cls.__name__} {model_id} not found"}), 404))
    
    return model

def send_slack_message(task):
    data = {
            "channel": "task-notifications",
            "text": f"Someone just completed the task {task.title}"
        }
    headers = {"Authorization": f"Bearer {slack_auth_key}"}
    requests.post(SLACK_BOT_API_URL, data=data, headers=headers)

@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json() 

    if "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()
    
    return jsonify({"task": new_task.to_dict()}), 201


@tasks_bp.route("", methods=["GET"])
def read_all_tasks():  
    sort_query = request.args.get("sort")
    task_query = Task.query

    if sort_query == "asc":
        task_query = task_query.order_by(Task.title.asc())
    if sort_query == "desc":
        task_query = task_query.order_by(Task.title.desc())

    tasks = task_query.all()

    tasks_response = [task.to_dict() for task in tasks]
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task(task_id):
    task = validate_model(Task, task_id)
    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json() 
    
    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}), 200

@tasks_bp.route("/<task_id>/<status>", methods=["PATCH"])
def mark_task_complete(task_id, status):
    task = validate_model(Task, task_id)

    if status == "mark_complete":
        task.completed_at = datetime.utcnow()
        send_slack_message(task)

    if status == "mark_incomplete":
        task.completed_at = None
    
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["GET"])
def read_all_goals():

    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response), 200

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json() 

    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({"goal": new_goal.to_dict()}), 201

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_task(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    
    goal.title = request_body["title"]
    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}), 200

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def add_tasks_to_goal(goal_id):
    request_body = request.get_json()

    goal = validate_model(Goal, goal_id)

    for task_id in request_body["task_ids"]:
        task = Task.query.get(task_id)
        goal.tasks.append(task)
    
    db.session.commit()

    return jsonify({"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}), 200
    
@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def read_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({"id": goal.goal_id, 
                    "title": goal.title,
                    "tasks": [task.to_dict() for task in goal.tasks]}), 200