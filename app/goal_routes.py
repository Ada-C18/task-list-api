
from flask import Blueprint, jsonify, request, make_response, abort
from app import db 
from app.models.goal import Goal
from app.models.task import Task



goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_task(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response(f'"details": invalid data'), 400)

    goal = Goal.query.get(goal_id)

    if not goal:
        response = f"goal not found"
        abort(make_response(jsonify({"message":response}), 404))

    
    return goal


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return{"goal":Goal.to_dict},201


@goals_bp.route("", methods=["GET"])
def get_goals():
    goals= Goal.query.all()

    goal_response = [goal.to_dict() for goal in goals]

  
    return jsonify(goal_response), 200
