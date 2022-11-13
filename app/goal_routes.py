from app import db
from app.models.task import Task
from app.models.goal import Goal
from flask import request, Blueprint, jsonify, make_response, abort
from sqlalchemy import desc
from datetime import datetime
import requests
import os

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

# goals
@goals_bp.route("", methods=["GET"])
def read_goals():
    goals = Goal.query.all()
    goals_list = []

    for goal in goals:
        goals_list.append(
            
            {"id": goal.goal_id, "title": goal.title}
        )
        
        # return jsonify(goals_list),200
    return jsonify(goals_list)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    validate_goal = validate_model(Goal, goal_id)

    goal = Goal.query.get(goal_id)
    if goal:
        return {
            "goal": goal.to_dict_goal()
        }, 200
    else:
        # return make_response(jsonify(None))
        return []

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        return jsonify({
            "details": "Invalid data"
        }), 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {
            "goal": new_goal.to_dict_goal()
        }, 201


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    print(request_body)

    db.session.commit()

    return make_response(jsonify(f"Updated Goal Title")) # {goal.goal_id}

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if goal:
        goal_dict = {
            "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
            # "details": f"Goal {goal_id} \"Build a habit of going outside daily\" successfully deleted"
            }

        db.session.delete(goal)
        db.session.commit()
        return jsonify(goal_dict), 200
    # return make_response(jsonify(f"Goal #{goal_dict} successfully deleted"))


    # if goal:
    #     goal_dict = {
    #     # "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    #     "details": f"Goal {goal_id} \"Build a habit of going outside daily\" successfully deleted"
    #     }
    # else:
    #     db.session.delete(goal)
    #     db.session.commit()

    #     return jsonify({"message": f"Goal {goal_id} not found"}), 404

    # db.session.delete(goal)
    # db.session.commit()

    # return jsonify(goal_dict), 200