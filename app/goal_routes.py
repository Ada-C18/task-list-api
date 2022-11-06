from app.models.goal import Goal
from flask import Blueprint, request, make_response, jsonify, abort
from app.models.task import Task
from .routes import *
from app import db
import datetime

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_goal(goal_id):
    goal_id = int(goal_id)
    
    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"message":f"Goal {goal_id} is not found"}, 404))

    return goal

@goal_bp.route("", methods=["POST"])
def create_goal():
    
    request_body = request.get_json()

    if not "title" in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_goal = Goal(title=request_body["title"]
        )

    db.session.add(new_goal)
    db.session.commit()
    
    return make_response({"goal": new_goal.to_json()},201)

@goal_bp.route("", methods=["GET"])
def get_goal_list():

    goals = Goal.query.all()

    goals_list = [goal.to_json() for goal in goals]

    return jsonify(goals_list)

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_goal(goal_id):

    goal = validate_goal(goal_id)

    return make_response({"goal":goal.to_json()})


@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goals(goal_id):

    goal = validate_goal(goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    return make_response({"goal": goal.to_json()})

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):

    goal = validate_goal(goal_id)

    db.session.delete(goal)

    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'})


