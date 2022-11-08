from app import db
from app.models.goal import Goal
from flask import Blueprint, request, make_response
from app.routes import validate_model

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        return make_response({"details" : "Invalid data"}, 400)
    
    new_goal = Goal.goal_from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal" :new_goal.goal_to_dict()}, 201