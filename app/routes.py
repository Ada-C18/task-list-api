from flask import Blueprint, jsonify, abort, request, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc
from .routes_helper import validate_id, validate_input
import datetime, os,requests

task_bp= Blueprint("task_bp", __name__, url_prefix="/tasks")
goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@task_bp.route("",methods=["GET"])
def get_all_tasks():
    sort_query= request.args.get("sort")
    
    if sort_query:
        if sort_query == "desc":
            tasks = Task.query.order_by(desc(Task.title))
        else:
            tasks = Task.query.order_by(Task.title)
    else:
        tasks = Task.query.all()

    all_tasks = []
    for task in tasks:
        all_tasks.append({
            "id": task.task_id,
            "title" : task.title,
            "description": task.description, 
            "is_complete": task.is_complete
        })
    return jsonify(all_tasks), 200

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task_by_id(task_id):
    task = validate_id(Task, task_id)

    return jsonify({"task": task.to_dict()}), 200

@task_bp.route("<task_id>", methods=["PUT"])
def update_one_task(task_id):
    task = validate_id(Task, task_id)

    request_body = request.get_json()
    task.title = request_body["title"]
    task.description= request_body["description"]
    
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 200

@task_bp.route("", methods=["POST"])
def create_new_task():
    request_body = request.get_json()
    validate_input(Task, request_body)
    task = Task.from_dict(request_body)

    db.session.add(task)
    db.session.commit()

    return jsonify({"task": task.to_dict()}), 201

@task_bp.route("<task_id>", methods=["DELETE"])
def delete_one_task(task_id):
    task=validate_id(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = datetime.datetime.today()
    task.is_complete = True

    db.session.commit()
    query_params={
        "channel": "task-list-notifications",
        "text": f"Someone just completed the task {task.title}"
    }
    header = {"Authorization": f"Bearer {os.environ.get('SLACK_TASK_BOT_KEY')}"}
    requests.get(os.environ.get("SLACK_POST_MESSAGE_PATH"), params=query_params, headers=header)

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description":task.description,
        "is_complete": task.is_complete
    }}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_id(Task, task_id)
    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description":task.description,
        "is_complete": task.is_complete
    }}), 200

@goal_bp.route("", methods=["POST"])
def create_new_goal():
    request_body = request.get_json()

    validate_input(Goal, request_body)
    goal = Goal.from_dict(request_body)

    db.session.add(goal)
    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 201

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    all_goals = []
    for goal in goals:
        all_goals.append(goal.to_dict())
    return jsonify(all_goals), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal_by_id(goal_id):
    goal = validate_id(Goal, goal_id)

    return jsonify({"goal": goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return jsonify({"goal": goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}

@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def assoc_tasks_with_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids = request_body["task_ids"]
    
    for task_id in task_ids:
        task = validate_id(Task, task_id)
        task.goal_id = goal_id
        db.session.commit()
    
    response = {
        "id": goal.goal_id, 
        "task_ids": task_ids
    }

    return jsonify(response),200

@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_from_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    response = {
        "id": goal.goal_id, 
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }

    return jsonify(response), 200