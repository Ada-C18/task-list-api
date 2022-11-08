from app import db
from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from datetime import datetime
import requests
import os

goal_bp = Blueprint("goal", __name__, url_prefix="/goals")

# validate 
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not a valid id"}, 400))
    
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

# read all tasks
@goal_bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    # goals_response = [goal.to_dict() for goal in goals]
    goals_response = []
    for goal in goals:
        goals_response.append(
            {
            "id": goal.goal_id,
            "title": goal.title
            }
        )
    return jsonify(goals_response)

# # read one task
@goal_bp.route("/<goal_id>", methods=["GET"])
def read_one_task(goal_id):
    goal = validate_model(Goal, goal_id)

    return { "goal": 
        {
        "id": goal.goal_id,
        "title": goal.title
        }
    }

# # create new task
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal(title=request_body["title"])
    except:
        return abort(make_response({"details": 'Invalid data'}, 400))

    db.session.add(new_goal)
    db.session.commit()

    return { "goal": 
        {
        "id": new_goal.goal_id,
        "title": new_goal.title
        }
    }, 201

# # update task
@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return { "goal": 
        {
        "id": goal.goal_id,
        "title": goal.title
        }
    }

# # delete task
@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}, 200)
