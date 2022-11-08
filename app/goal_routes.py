from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.task import Task
from app.models.goal import Goal
from app.task_routes import validate_model
from datetime import date

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

@goal_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)
    
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_dict()}), 201


@goal_bp.route('', methods=['GET'])
def get_or_sort_goals():
    goals = Goal.query.all() 
    result = []
    for goal in goals:
        result.append(goal.to_dict())
    
    return jsonify(result), 200


@goal_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):
    goal_chosen = validate_model(Goal, goal_id)

    return jsonify({"goal":goal_chosen.to_dict()}), 200


@goal_bp.route('/<goal_id>', methods=['PUT'])
def update_one_goal(goal_id):
    update_goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    update_goal.title = request_body["title"]

    db.session.commit()

    return jsonify({"goal": update_goal.to_dict()}), 200
