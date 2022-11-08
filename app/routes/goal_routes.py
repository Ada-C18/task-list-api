from flask import Blueprint, request, make_response, jsonify
from app import db
from app.models.goal import Goal


goal_bp = Blueprint('goal_bp', __name__, url_prefix='/goals')


@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    goal_response = [{"id": goal.goal_id,"title": goal.title}for goal in goals]

    return jsonfiy(goal_response)


