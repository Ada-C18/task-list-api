from flask import Blueprint, jsonify, make_response, request, abort
from .models.goal import Goal
from .models.task import Task
from .task_routes import validate_model, put_or_patch_model
from app import db
import requests, os

# ===================
# BLUEPRINTS
# ===================

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# ===================
# ROUTES
# ===================

@goals_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.new_instance_from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        return {"goal": new_goal.create_dict()}, 201

    except KeyError:
        return {"details": "Invalid data"}, 400

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        goals = Goal.query.filter_by(title=title_query)
    elif sort_query == "asc":
        goals = Goal.query.order_by(Goal.title.asc()).all()
    elif sort_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc()).all()
    else:
        goals = Goal.query.all()

    goals_response = [goal.create_dict() for goal in goals]

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = {"goal": goal.create_dict()}
    return make_response(response)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    return put_or_patch_model(Goal, goal_id)

@goals_bp.route("/<goal_id>", methods=["PATCH"])
def patch_goal(goal_id):
    return put_or_patch_model(Goal, goal_id)

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}

@goals_bp.route("/<goal_id>/tasks", methods=["POST"])
def post_tasks_to_goal(goal_id):

    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_id_in = Task.task_id.in_(request_body["task_ids"])
    goal.tasks += Task.query.filter(task_id_in).all()
    
    db.session.commit()
    return {"id": goal.goal_id, "task_ids": [task.task_id for task in goal.tasks]}

@goals_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return goal.create_dict(tasks=True)

        
    
    
