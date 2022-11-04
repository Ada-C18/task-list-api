from flask import Blueprint, jsonify, make_response, request, abort,Response
from app import db
from app.models import goal
from app.models.goal import Goal


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        abort(make_response(jsonify({"message": "goal_id must be an integer"}),400))
    
    matching_goal = Goal.query.get(goal_id)

    if matching_goal is None:
        response_str = f"Goal with id {goal_id} was not found in the database."
        abort(make_response(jsonify({"message": response_str}), 404))

    return matching_goal


@goal_bp.route("", methods = ["POST"])
def add_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return jsonify({"details": "Invalid data"}),400

    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    goal_dict = new_goal.to_dict()

    return jsonify({"goal":goal_dict}),201

@goal_bp.route("", methods=["GET"])
def get_all_goals():

    title_query = request.args.get("title")
    sort_at_query = request.args.get("sort")

    if title_query:
        goals = Goal.query.filter_by(title = title_query)
    elif sort_at_query == "asc":
        goals = Goal.query.order_by(Goal.title)
    elif sort_at_query == "desc":
        goals = Goal.query.order_by(Goal.title.desc())
    else:
        goals = Goal.query.all()
    response = []
    for goal in goals:
        response.append(goal.to_dict())
    return jsonify(response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_goal_id(goal_id)
    goal_dict = goal.to_dict()
    
    return jsonify({"goal":goal_dict})

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    if "title" not in request_body:
                return jsonify({"message":"Request must include title"}),400

    goal.title = request_body["title"]

    goal_dict = goal.to_dict()

    db.session.commit()
    return jsonify({"goal":goal_dict}),200

@goal_bp.route("/<goal_id>",methods = ['DELETE'])
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return jsonify({"details":f"Goal {goal.goal_id} \"{goal.title}\" successfully deleted"}),200
