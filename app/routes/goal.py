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
