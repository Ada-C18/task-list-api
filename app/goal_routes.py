from app import db
from .models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goals(goal_id):
    try:
        goal_id = int(goal_id )
    except:
        abort(make_response({"message":f"Goal {goal_id} invalid"}, 400))

    goal = Goal.query.get(goal_id )

    if not goal:
        abort(make_response({"message":f"goal {goal_id} not found"}, 404))
    
    return goal

@goals_bp.route("", methods=["POST"])
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal(
            title=request_body["title"]
            )
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400

    db.session.add(new_goal)
    db.session.commit()
    
    return jsonify({"goal": new_goal.to_dict()}), 201


@goals_bp.route("", methods=["GET"])
def read_all_goals():
    goal_param = request.args
    goals = Goal.query.all()
    goals_response = []
    for goal in goals:
        goals_response.append({
            "id": goal.goal_id,
            "title": goal.title
        })

    return jsonify(goals_response)

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goals(goal_id)
    return jsonify(goal.to_dict()), 200


@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goals(goal_id)
    title = request.json.get("title")
    
    if not title:
        return jsonify({"details": "Invalid data"}), 400

    goal.title = title
    db.session.commit()
    return jsonify(goal.to_dict()["goal"]), 200
    

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goals(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"}), 200




