from flask import Blueprint, request, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from operator import itemgetter
from datetime import date
import requests
import os

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")
#-------------------------------------------HELPERS----------------------------------
def validate_goal(input_goal_id):
    try:
        input_goal_id = int(input_goal_id)
    except:
        abort(make_response({"message": f"Goal {input_goal_id} is not a valid id"}, 400))

    goal = Goal.query.get(input_goal_id)

    if not goal:
        abort(make_response({"message": f"Goal {input_goal_id} does not exist"}, 404))

    return goal

#-------------------------------------------POST----------------------------------
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
        
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
        "id": new_goal.goal_id,
        "title": new_goal.title
    }}, 201

#-------------------------------------------GET----------------------------------
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    response  = []
    for goal in goals:
        goal_dict = {
            "id": goal.goal_id,
            "title": goal.title
    }
        response.append(goal_dict)

    return jsonify(response), 200

@goal_bp.route("/<input_goal_id>", methods=["GET"])
def get_one_goal(input_goal_id):
    goal = validate_goal(input_goal_id)

    return {
        "goal": {
            "id": goal.goal_id,
            "title": goal.title
        }
  }
#-------------------------------------------PUT----------------------------------


#-------------------------------------------PATCH----------------------------------


#-------------------------------------------DELETE----------------------------------