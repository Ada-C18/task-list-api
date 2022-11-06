from flask import Blueprint, request, jsonify, abort, make_response, request
from app import db
from app.models.goal import Goal
from .task_routes import validate_object


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")
#-------------------------------------------HELPERS----------------------------------

#-------------------------------------------POST----------------------------------
@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
        
    new_goal = Goal(
        title=request_body["title"]
    )

    db.session.add(new_goal)
    db.session.commit()

    return {
        "goal": new_goal.to_dict()}, 201

#-------------------------------------------GET----------------------------------
@goal_bp.route("", methods=["GET"])
def get_all_goals():
    goals = Goal.query.all()

    response  = []
    for goal in goals:
        goal_dict = goal.to_dict()
        response.append(goal_dict)

    return jsonify(response), 200

@goal_bp.route("/<input_goal_id>", methods=["GET"])
def get_one_goal(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id)

    return {
        "goal": chosen_goal.to_dict()
}
#-------------------------------------------PUT----------------------------------
@goal_bp.route("/<input_goal_id>", methods=["PUT"])
def update_one_goal(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id) #current goal in db
    request_body = request.get_json() #what client wants to change

    chosen_goal.title = request_body["title"]

    db.session.commit()
    
    return {"goal": chosen_goal.to_dict()}

#-------------------------------------------PATCH----------------------------------

#-------------------------------------------DELETE----------------------------------
@goal_bp.route("/<input_goal_id>", methods=["DELETE"])
def delete_goal(input_goal_id):
    chosen_goal = validate_object(Goal, input_goal_id)

    db.session.delete(chosen_goal)
    db.session.commit()

    return {
        "details": f"Goal {input_goal_id} \"{chosen_goal.title}\" successfully deleted"
}