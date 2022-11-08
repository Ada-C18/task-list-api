from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.models.goal import Goal
from app.routes.task import get_task_from_id

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")


@goal_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    try:
        new_goal= Goal(title=request_body['title'])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400 
    db.session.add(new_goal)
    db.session.commit()
    return jsonify(new_goal.to_response()), 201


@goal_bp.route('', methods=['GET'])
def get_all_goals():
    goals = Goal.query.all()
    result = []
    for item in goals:
        result.append(item.to_dict())
    return jsonify(result), 200