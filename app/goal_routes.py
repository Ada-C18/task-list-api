from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort
from app import db


goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goal_bp.route("", methods =["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.from_goal_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()


    return make_response({"goal":(new_goal.to_goal_dict())}, 201)

@goal_bp.route("", methods = ["GET"])
def read_all_goals():
    task_query = Goal.query
    goals = task_query.all()
    
    all_goals = [goal.to_goal_dict() for goal in goals]

    return jsonify(all_goals), 200