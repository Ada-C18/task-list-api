from flask import Blueprint, request, make_response, jsonify, abort
from app import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc
from datetime import datetime
# import requests
# import os
# from dotenv import load_dotenv

# load_dotenv()

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model

#CREATE
@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return make_response(jsonify({"details": "Invalid data"}), 400)

    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

#READ
@goals_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response(jsonify({"goal": goal.to_dict()}), 200)

#UPDATE
@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    return make_response(jsonify({"goal": goal.to_dict()}), 200)

#DELETE
@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return make_response(jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200)