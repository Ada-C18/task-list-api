from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, request, make_response, abort
from app.routes.task import validate_model
import requests
import os

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()

        goal_dict = new_goal.to_dict()

        return make_response(jsonify({
            "goal": goal_dict}), 201)
    
    except:
        abort(make_response({"details": "Invalid data"}, 400))

@bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200

@bp.route("<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return make_response(jsonify({
        "goal": goal.to_dict()
    }))

@bp.route("<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({
        "goal": goal.to_dict()
    }))