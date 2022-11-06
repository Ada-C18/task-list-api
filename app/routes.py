from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import asc, desc
from datetime import datetime
import os
import requests

slack_oauth_token = os.environ.get("SLACK_OAUTH_TOKEN")

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response(({"msg": f"{task_id} is not valid"}), 400))

    task = Task.query.get(task_id)

    if not task:
        abort(make_response(({"msg": f"{task_id} not found"}), 404))

    return task

@tasks_bp.route("", methods=["GET"])
def read_all_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:
        tasks = Task.query.all()
    
    response = []
    for task in tasks:
            response.append(task.to_dict())
    
    return jsonify(response), 200


@tasks_bp.route("", methods=["POST"])
def create_one_task():
    request_body = request.get_json()

    try:
        new_task = Task(title=request_body["title"], description=request_body["description"])
            
    except Exception as e:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@tasks_bp.route("/<task_id>", methods=["GET"])
def read_one_task_by_id(task_id):
    task = validate_task_id(task_id)
    return {"task": task.to_dict()}


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_one_task_by_id(task_id):
    request_body = request.get_json()
    task = validate_task_id(task_id)

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task_by_id(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f"Task {task_id} \"Go on my daily walk 🏞\" successfully deleted"}), 200

@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_task_id(task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    # slack api call to post to task-notifications
    url = "https://slack.com/api/chat.postMessage"

    params = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    headers = {"Authorization": f"Bearer {slack_oauth_token}"}

    response = requests.patch(url=url, params=params, headers=headers)

    return {"task": task.to_dict()}

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_task_id(task_id)

    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}


####################Goal routes###################
def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response(({"msg": f"{goal_id} is not valid"}), 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response(({"msg": f"{goal_id} not found"}), 404))

    return goal

@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except Exception as e:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()
    
    response = []
    for goal in goals:
            response.append(goal.to_dict())
    
    return jsonify(response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal_by_id(goal_id):
    goal = validate_goal_id(goal_id)
    return {"goal": goal.to_dict()}


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal_by_id(goal_id):
    request_body = request.get_json()
    goal = validate_goal_id(goal_id)

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal_by_id(goal_id):
    goal = validate_goal_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}), 200



@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_existing_tasks_to_goal_id(goal_id):
    request_body = request.get_json()
    goal = validate_goal_id(goal_id)

    provided_task_ids = request_body["tasks"]

    tasks = Task.query.filter(Task.task_id.in_(provided_task_ids)).all()
    
    task_ids = [task.task_id for task in tasks]
    # goal.tasks = task_ids
    
    for task in tasks:
        task.goal_id = goal_id

    db.session.commit()
    
    return jsonify({
        "id": goal.goal_id,
        "task_id": task_ids
        })

@goals_bp.route(""/<goal_id>/tasks"", methods=["GET"])
def read_all_tasks_by_goal_id():
    goal = validate_goal_id


