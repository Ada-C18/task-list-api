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

@goals_bp.route("", methods=['POST'])
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