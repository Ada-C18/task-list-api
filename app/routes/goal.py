from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, make_response, request, abort

goals_bp = Blueprint("goal", __name__, url_prefix="/goals")

# HELPER FUNCTIONS
def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not a valid id"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    
    return model

# CREATE
@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()

    created_goal = {"goal": new_goal.to_dict()}
    return make_response(created_goal, 201)