from flask import Blueprint, jsonify, abort, make_response, request
from datetime import datetime
from app import db
from app.models.goal import Goal

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_complete_request(request_body):
    try:
        if request_body["title"]:
            return request_body

    except:
        abort(make_response({"details": "Invalid data"}, 400))


def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)    
    except:
        abort(make_response({"details": "Invalid data"}, 404))

    goal = Goal.query.get(goal_id)

    if not goal:
        abort(make_response({"details": "Invalid data"}, 404))
    
    return goal


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    valid_data = validate_complete_request(request_body)
    new_goal = Goal.from_dict(valid_data)

    db.session.add(new_goal)
    db.session.commit()

    goal_response = {
        "goal": new_goal.to_dict()
    }
    return make_response(jsonify(goal_response), 201)


@goals_bp.route("", methods=["GET"])
def get_all_goals_sort_asc():
    goal_query = Goal.query.all()
    title_query = request.args.get("title")
    if title_query:
        goal_query = Goal.query.filter_by(title=title_query)

    goals = goal_query

    goals_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goals_response), 200)


@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal_id(goal_id)

    goal_response = {
        "goal": goal.to_dict()
    }

    return make_response(jsonify(goal_response), 200)

@goals_bp.route("/<goal_id>", methods=["PUT"])
def goal_update_entire_entry(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    goal_response = {
        "goal": goal.to_dict()
    }

    return make_response((goal_response), 200)


@goals_bp.route("/<goal_id>", methods=["DELETE"])
def goal_delete(goal_id):
    goal = validate_goal_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({'details': f'Goal {goal.id} "{goal.title}" successfully deleted'}, 200)