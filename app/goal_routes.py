from flask import Blueprint, request, make_response, abort, jsonify
from app.models.goal import Goal
from app import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix = "/goals")

# HELPER FUNCTION
def validate_id(class_obj, id):
    try:
        object_id = int(id)
    except:
        abort(make_response({"details": f"{class_obj} {id} is invalid"}, 400))

    query_result = class_obj.query.get(object_id)
    if not query_result:
        abort(make_response({"details": f"{class_obj} {id} is not found"}, 404))
    
    return query_result

# CREATE RESOURCE
@goals_bp.route("", methods = ["POST"])
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_json(request_body)
    except KeyError:
        return make_response({"details": "Invalid data"}, 400)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(new_goal.to_dict(), 201)

# GET ALL RESOURCE
@goals_bp.route("", methods = ["GET"])
def get_all_goal():
    goals_response = []

    goals = Goal.query.all()

    for goal in goals:
        goals_response.append(goal.to_dict()["goal"])

    return jsonify(goals_response), 200

# GET ONE RESOURCE
@goals_bp.route("/<goal_id>", methods = ["GET"])
def get_one_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    return jsonify(goal.to_dict()), 200


# UPDATE RESOURCE
@goals_bp.route("/<goal_id>", methods = ["PUT"])
def update_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    request_body = request.get_json()

    goal.update(request_body)

    db.session.commit()

    return make_response(goal.to_dict())

# DELETE RESOURCE
@goals_bp.route("/<goal_id>", methods = ["DELETE"])
def delete_goal(goal_id):
    goal = validate_id(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {goal_id} "{goal.title}" successfully deleted'})