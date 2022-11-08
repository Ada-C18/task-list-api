from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request


goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.route("", methods=["POST"])
def create_goal():

    request_body = request.get_json() 
    new_goal = Goal(
        title=request_body["title"]
        )
    
    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": {
            "id": new_goal.goal_id,
            "title": new_goal.title,
        }
        }