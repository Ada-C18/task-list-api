from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

#helper function to get goal by id:  ----> needs to be refactored.
def get_goal_from_id(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        return abort(make_response({"msg":f"Invalid data type: {goal_id}"}, 400))
    chosen_goal = Goal.query.get(goal_id)

    if chosen_goal is None:
        return abort(make_response({"msg": f"Could not find goal item with id: {goal_id}"}, 404))
    return chosen_goal

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}),201

@goals_bp.route("", methods=['GET'])
def get_all_goals():
#------retomar aqui !
    goals = Goal.query.all()
    goals_response = []

    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())
    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = get_goal_from_id(goal_id)
    return jsonify({
        "goal": goal.to_dict()
    })

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    request_body = request.get_json()
    goal = get_goal_from_id(goal_id)

    if "title" not in request_body:
        return jsonify({"msg": "Request must include a title"}),400

    goal.title = request_body["title"]

    db.session.commit()

    return jsonify({
        "goal": goal.to_dict()
    })

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = get_goal_from_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return jsonify({
        "details": f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"
        })