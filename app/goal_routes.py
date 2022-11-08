from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request,abort
from sqlalchemy import desc, asc

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))
        
    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))
    return model


@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details": "Invalid data"},400)
    new_goal = Goal(title=request_body["title"])

    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal":new_goal.to_dict()},201

@goals_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    
    goals_response = []
    for goal in goals:
        goals_response.append(goal.to_dict())

    return jsonify(goals_response)
    # return [{"task":tasks.to_dict()}]

@goals_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    return {"goal":goal.to_dict()},200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    return {'details': f'Goal {goal.goal_id} "{goal.title}" successfully deleted'}

# @goals_bp.route("/<goal_id>", methods=["PUT"])
# def update_goal(goal_id):
#     goal = validate_model(Goal,goal_id)

#     request_body = request.get_json()
#     # if "title" not in request_body:
#     #     request_body["title"]= None

#     goal.title = request_body["title"]

#     db.session.commit()

#     return {"goal":goal.to_dict()}