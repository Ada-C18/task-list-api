from flask import Blueprint, jsonify, make_response, request, abort
from app import db
from app.models.goal import Goal
import datetime

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


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError:
        return make_response(jsonify({
            "details": "Invalid data"
            }), 400)
    
    db.session.add(new_goal)
    db.session.commit()

    goal_response = {
        "goal": new_goal.to_dict()
    }

    return make_response(jsonify(goal_response), 201)

@goals_bp.route("", methods=["GET"])
def read_all_goals():
    title_query = request.args.get("title")
    goal_query = Goal.query

    if title_query:
        goal_query = goal_query.filter_by(title=title_query)

    goals = goal_query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)


@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_response = {
        "goal": goal.to_dict()
    }

    return make_response(jsonify(goal_response), 200)


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    goal_response = {
        "goal": goal.to_dict()
    }

    return make_response(jsonify(goal_response), 200)


@goals_bp.route("<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    goal_response = {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }

    return make_response(jsonify(goal_response), 200)