from datetime import datetime
from app import db
from app.models.goal import Goal
from app.routes.routes_helper import validate_model, validate_input_data, error_message
from flask import Blueprint, jsonify, make_response, request, abort

goals_bp = Blueprint('goals_bp', __name__, url_prefix='/goals')

# create a goal (POST)
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    new_goal = validate_input_data(Goal, request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

# read one goal (GET)
@goals_bp.route("/<id>", methods=["GET"])
def read_one_goal(id):
    goal = validate_model(Goal, id)

    return jsonify({"goal": goal.to_dict()}), 200
    
# read all goals (GET)
@goals_bp.route("", methods=["GET"])
def read_all_goals():

    goals = Goal.query.all()

    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response)

# replace a goal (PUT)
@goals_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.update(request_body)
    db.session.commit()
    
    response = {"goal": goal.to_dict()}
    return response


@goals_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)
    title = str(goal.title)
    db.session.delete(goal)
    db.session.commit()

    # Returns error 
    return(make_response({"details": f"Goal {id} \"{title}\" successfully deleted"}), 200)
