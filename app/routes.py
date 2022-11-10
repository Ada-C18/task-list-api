from flask import Blueprint, request, jsonify, abort, make_response
from . import db
from .models.task import Task
from .models.goal import Goal
from datetime import datetime


"""
task routes
"""

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"msg": f"Task {task_id} invalid"}, 400))
    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"msg": f"Task {task_id} not found"}, 404))
    return task

@tasks_bp.route("", methods=['POST'])
def add_task():
    request_body = request.get_json()
    if 'title' not in request_body or 'description' not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task.from_dict(request_body)

    if 'completed_at' not in request_body and new_task.completed_at:
        abort(make_response({"details": "Invalid data"}, 400))

    db.session.add(new_task)
    db.session.commit()

    is_complete = False
    if new_task.completed_at:
        is_complete = True
    
    return {"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": is_complete
    }}, 201

@tasks_bp.route("", methods=['GET'])
def get_tasks():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    response = []
    for task in tasks:
        is_complete = False
        if task.completed_at:
            is_complete = True
        response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete
        })
    
    return jsonify(response), 200

@tasks_bp.route("/<task_id>", methods=['GET'])
def get_one_task(task_id):
    task = validate_task(task_id)

    is_complete = False
    if task.completed_at:
        is_complete = True
    return {"task": {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete}}, 200

@tasks_bp.route("/<task_id>", methods=['PUT'])
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()
    try:
        task.title = request_body["title"]
        task.description = request_body["description"]
    except:
        raise KeyError("Either task title or description is missing from your input")
    db.session.commit()

    is_complete = False
    if task.completed_at:
        is_complete = True
    return {"task": {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete}}, 200

@tasks_bp.route("/<task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = validate_task(task_id)
    title = task.title
    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {task_id} "{title}" successfully deleted'}, 200

@tasks_bp.route("/<task_id>/mark_complete", methods=['PATCH'])
def mark_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    is_complete = False
    if task.completed_at:
        is_complete = True
    return {"task": {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete}}, 200

@tasks_bp.route("/<task_id>/mark_incomplete", methods=['PATCH'])
def mark_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()

    is_complete = False
    if task.completed_at:
        is_complete = True
    return {"task": {"id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": is_complete}}, 200

"""
goals routes
"""
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"msg": f"Goal {goal_id} invalid"}, 400))
    goal = Goal.query.get(goal_id)
    if not goal:
        abort(make_response({"msg": f"Goal {goal_id} not found"}, 404))
    return goal

@goals_bp.route("", methods=['POST'])
def add_goal():
    request_body = request.get_json()
    if 'title' not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title,
    }}, 201

@goals_bp.route("", methods=['GET'])
def get_goals():
    goals = Goal.query.all()

    response = []
    for goal in goals:
        response.append({"id": goal.goal_id,
                        "title": goal.title})

    return jsonify(response), 200

@goals_bp.route("/<goal_id>", methods=['GET'])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {"goal": {"id": goal.goal_id,
            "title": goal.title}}, 200

@goals_bp.route("/<goal_id>", methods=['PUT'])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    try:
        goal.title = request_body["title"]
    except:
        raise KeyError("Goal title is missing from your input")
    db.session.commit()

    return {"goal": {"id": goal.goal_id,
            "title": goal.title}}, 200

@goals_bp.route("/<goal_id>", methods=['DELETE'])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    title = goal.title
    db.session.delete(goal)
    db.session.commit()
    return {"details": f'Goal {goal_id} "{title}" successfully deleted'}, 200