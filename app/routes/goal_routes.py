from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.task import Task
from app.models.goal import Goal
import requests
import os


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"Message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if not request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201


@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goal_query = Goal.query
    goals = goal_query.all()
    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response), 200


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal_id} {goal.title} successfully deleted"}, 200
