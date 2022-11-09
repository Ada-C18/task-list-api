
from app import db
from app.models.goal import Goal
from app.models.task import Task
from flask import Blueprint, jsonify, make_response, request, abort
from app.routes.helper_functions import validate_model

bp = Blueprint("goals", __name__, url_prefix="/goals")

@bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if not request_body:
        abort(make_response({"details": "Invalid Data"}, 400))


    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(f"Goal {new_goal.title} successfully created", 201)

@bp.route("", methods=["GET"])
def read_all_goals():
    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]

    return jsonify(goals_response)

@bp.route("/<goal_id>/", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return make_response(dict(goal = goal.to_dict()), 200)

@bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    goal.title = request_body["title"]

    db.session.commit()
    return make_response(dict(goal = goal.to_dict()), 200)

@bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()  
    return make_response({'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}, 200)