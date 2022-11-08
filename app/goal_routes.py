from app import db
from app.models.goal import Goal
from flask import abort, Blueprint, jsonify, make_response, request
import os

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"msg":f"Task {goal_id} not found"}, 404))

    return goal

def get_goal_from_id(goal_id):
    chosen_goal = Goal.query.get(goal_id)
    if chosen_goal is None:
        return abort(make_response({"msg": f"Could not find goal item with id: {goal_id}"}, 404))
    return chosen_goal

@goals_bp.route("", methods=["POST"])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal=Goal(
            title=request_body["title"]
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_goal)
    db.session.commit()
    return jsonify({"goal":new_goal.to_dict()}), 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    result = [goal.to_dict() for goal in goals]
    return jsonify(result), 200

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):
    chosen_goal = get_goal_from_id(goal_id)
    return jsonify({"goal":chosen_goal.to_dict()}), 200