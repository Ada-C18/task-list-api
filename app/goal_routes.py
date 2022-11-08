from app import db
from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify
from app.routes import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details" : "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal" :new_goal.to_dict()}, 201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goal_response = []
    for goal in goals:
        goal_response.append(goal.to_dict())
    return jsonify(goal_response)