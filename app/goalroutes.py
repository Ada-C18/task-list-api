from app import db
from app.models.goal import Goal
from .routes import validate_model
from flask import Blueprint, request, make_response, jsonify

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return {"goal":new_goal.to_dict()}, 201

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    
    return jsonify(goals_response)

@goals_bp.route("/<model_id>", methods=["GET"])
def read_one_goal(model_id):
    goal = validate_model(Goal, model_id)
    return {"goal":goal.to_dict()}, 200

@goals_bp.route("/<model_id>", methods=["PUT"])
def update_goal(model_id):
    goal = validate_model(Goal, model_id)
    
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal":goal.to_dict()}, 200
