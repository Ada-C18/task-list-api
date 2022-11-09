from app import db
from app.models.goal import Goal
from flask import Blueprint,jsonify, make_response, request, abort

goal_bp = Blueprint("goals", __name__, url_prefix="/goals")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model
def validate_dict(request_body):
    request_body = dict(request_body)
    if not (request_body.get("title", False)):
        abort(make_response({"details": "Invalid data"},400))
    return request_body

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    goal_dict= validate_dict(request_body)
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)

@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()
    goal_response = [goal.to_dict() for goal in goals]

    return make_response(jsonify(goal_response), 200)

@goal_bp.route("/<id>", methods=["GET"])
def get_goal(id):
    goal = validate_model(Goal, id)
    response_body = {"goal": goal.to_dict()}
    return make_response(jsonify(response_body), 200)

@goal_bp.route("/<id>", methods=["PUT"])
def update_goal(id):
    goal = validate_model(Goal, id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return make_response(jsonify({"goal": goal.to_dict()}), 200)

@goal_bp.route("/<id>", methods=["DELETE"])
def delete_goal(id):
    goal = validate_model(Goal, id)
    
    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f'Goal {id} "{goal.title}" successfully deleted'}),200
