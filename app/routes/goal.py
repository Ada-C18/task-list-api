from app import db 
from app.models.goal import Goal
from flask import Flask, Blueprint, jsonify, make_response, request, abort
from datetime import datetime as dt
from app.routes.task import validate_model
import requests

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

#purpose: create goal.reminder to refactor
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = new_goal.to_dict()

    return make_response(jsonify({
        "goal":goal_dict }), 201)

#purpose: get saved goals
@goals_bp.route("", methods=["GET"])
def retrieve_goals():
    goals = Goal.query.all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response), 200
