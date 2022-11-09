from flask import Blueprint, jsonify, make_response, request, abort
from .models.goal import Goal
from app import db
import datetime, requests, os

# ===================
# BLUEPRINTS
# ===================

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

# ===================
# HELPER FUNCTIONS
# ===================

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response({"message": f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

    return goal

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
    goal = validate_goal(goal_id)
    response = {"goal": goal.create_dict()}
    return make_response(response)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.update(request_body)

    db.session.commit()

    return {"goal": goal.create_dict()}

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}