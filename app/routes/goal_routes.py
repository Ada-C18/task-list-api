from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, request, jsonify, make_response
from app.routes.task_routes import validate_id

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

# ================================
# Create one goal 
# ================================

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal(title=request_body["title"])
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_json()}), 201

# ==================================
# Get all goals  
# ==================================

@goal_bp.route("", methods=["GET"])
def get_all_goals():
        all_goals = Goal.query.all()
        results_list = []
        for goal in all_goals:
            results_list.append(goal.to_json())
        return jsonify(results_list), 200

# ==================================
# Get one goal by id number
# ==================================

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    return jsonify({"goal": validate_id(Goal, goal_id).to_json()}), 200

# ==================================
# Update one goal 
# ==================================

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_one_goal(goal_id):
    request_body = request.get_json()
    goal = validate_id(Goal, goal_id)
    goal.update(request_body)
    db.session.commit()
    return jsonify({"goal": goal.to_json()}), 200

# ==================================
# Delete one goal by id
# ==================================

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details":f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)

# ======================================
# Get all tasks that are under one goal
# ======================================
@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_all_tasks_for_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)
    all_goal_tasks = []
    for task in goal.tasks:
        all_goal_tasks.append(Task.to_json(task))
    return make_response({"id": goal.goal_id, "title": goal.title, "tasks": all_goal_tasks}, 200)

# ======================================
# Post tasks to one goal
# ======================================
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def associate_tasks_with_one_goal(goal_id):
    request_body = request.get_json()
    goal = validate_id(Goal,goal_id)
    task_list = request_body["task_ids"]
    for task_number in task_list:
        task = validate_id(Task, task_number)
        if task not in goal.tasks:
            goal.tasks.append(task)
    db.session.commit()
    return make_response({"id": goal.goal_id, "task_ids": task_list}, 200)