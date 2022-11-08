from app import db
from app.models.goal import Goal
from .route_helpers import validate_model, send_slack_message
from flask import Blueprint, jsonify, abort, make_response, request

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
# Creates a new goal and returns it as json
def create_new_goal():
    request_body = request.get_json()
    if "title" in request_body:
        new_goal = Goal.from_dict(request_body)

        db.session.add(new_goal)
        db.session.commit()
        return {"goal": new_goal.as_dict()}, 201
    else:
        return {"details": "Invalid data"}, 400