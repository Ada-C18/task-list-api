from flask import Blueprint, jsonify, abort, make_response, request
from app.models.goal import Goal
from app import db

goal_bp = Blueprint("goal_bp", __name__, url_prefix = "/goals")

@goal_bp.route("", methods = ["POST"])
def post_new_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        response_str = "Invalid data"
        abort(make_response({"details":response_str}, 400))
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    goal_dict = new_goal.make_dict()
    response = {"goal": goal_dict}
    return make_response(response, 201)

@goal_bp.route("", methods = ["GET"])
def get_all_goals():
    goals = Goal.query.all()
    response = []
    for goal in goals:
        goal_dict = goal.make_dict()
        response.append(goal_dict)
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    goal_dict = goal.make_dict()
    return make_response({"goal": goal_dict}, 200)

@goal_bp.route("/<goal_id>", methods = ["PUT", "PATCH"])
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    #This could be a helper function----#
    if "title" in request_body:
        goal.title = request_body["title"]
    else:
        response_str = f"You must include an updated goal title"
        abort(make_response({"message": response_str}, 400))
    #end a helper function#
    db.session.commit()
    response = {"goal": goal.make_dict()}
    return make_response(response, 200)
    

#ideally, combine this with validate task, passing in the class as well. 
def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response_str = f"Goal {goal_id} must be an integer"
        abort(make_response({"message": response_str}, 400))
    goal = Goal.query.get(goal_id)
    if not goal:
        response_str = f"Goal {goal_id} not found"
        abort(make_response({"message": response_str}, 404))
    return goal