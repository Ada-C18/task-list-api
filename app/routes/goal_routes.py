from app import db
from app.models.goal import Goal
from flask import abort, Blueprint, jsonify, make_response, request
# from dotenv import load_dotenv
# import os

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response({"details": "Invalid data"}, 400))

    goal = Goal.query.get(goal_id)

    if not goal:
        response_str = f"Goal {goal_id} not found."

        abort(make_response({"message": response_str}, 404))

    return goal


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    chosen_goal = validate_goal(goal_id)

    response = {
        "task": chosen_goal.to_dict()
    }

    return jsonify(response)
