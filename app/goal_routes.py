from flask import Blueprint
from flask import Blueprint, jsonify, request, abort, make_response
from app import db
from app.routes import get_model_from_id
from app.models.goal import Goal 

goal_bp = Blueprint("goals", __name__,url_prefix="/goals")


@goal_bp.route('', methods=['POST'])
def create_one_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return abort(make_response({"details": "Invalid data"}, 400))

    new_goal= Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal":new_goal.to_dict()}), 201


@goal_bp.route('', methods=['GET'])
def get_all_goals():

    goals= Goal.query.all()

    result = []

    for goal in goals:
        result.append(goal.to_dict())
    
    return jsonify(result), 200

@goal_bp.route('/<goal_id>', methods=['GET'])
def get_one_goal(goal_id):

    chosen_goal = get_model_from_id(Goal, goal_id)

    return jsonify({"goal":chosen_goal.to_dict()}), 200

@goal_bp.route('/<goal_id>', methods=['PUT'])
def update_one_goal(goal_id):
    update_goal = get_model_from_id(Goal, goal_id)

    request_body = request.get_json()

    try:
        update_goal.title = request_body["title"]

    except KeyError:
        return jsonify ({"msg": f"Missing attributes"}), 400

    db.session.commit()
    return jsonify({"goal":update_goal.to_dict()}), 200


@goal_bp.route('/<goal_id>', methods=['DELETE'])
def delete_one_goal(goal_id):
    goal_to_delete = get_model_from_id(Goal, goal_id)

    title_goal_to_delete= get_model_from_id(Goal, goal_id).to_dict()["title"]

    db.session.delete(goal_to_delete)
    db.session.commit()

    return jsonify({"details": f'Goal {goal_id} "{title_goal_to_delete}" successfully deleted'}), 200