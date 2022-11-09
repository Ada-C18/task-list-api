from os import abort
import os
from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
import requests
from requests import post
from datetime import datetime, timezone

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

def validate_goal(class_obj, goal_id):
    try:
        goal_id = int(goal_id)
    except:
        abort(make_response(jsonify({"message": f"Goal {goal_id} has an invalid goal_id"}), 400))

    query_result = class_obj.query.get(goal_id)

    if not query_result:
        abort(make_response({"message": f"Goal {goal_id} not found"}, 404))

    return query_result

@goals_bp.route("", methods=["GET"])
def read_all_goals():
#     color_param =request.args.get("color")
#     name_param = request.args.get("name")
    
#     if color_param:
#         goals = goal.query.filter_by(color=color_param)
#     elif name_param:
#         goals = goal.query.filter_by(name=name_param)
#     else:
#         goals = goal.query.all()

    goals = Goal.query.all()
    goals_response = []

    for goal in goals:
        goals_response.append(goal.to_dict())
        #big question if we need all the params 
        # or we need to exclude COMPLETED_AT????
        # I've removed completed_at from to_dict
        # for now, commented it out
    
    sorting_query = request.args.get("sort")
    if sorting_query == "asc":
        goals_response = sorted(goals_response, key=lambda dict: dict["title"])
    elif sorting_query == "desc":
        goals_response = sorted(goals_response, key=lambda dict: dict["title"], reverse=True) 
            
    return jsonify(goals_response), 200
    
@goals_bp.route("", methods=["POST"])
def create_goal():
    #need to validate goal
    request_body = request.get_json()
    print(request_body)
    # if request_body["title"] and request_body["description"]:
    if "title" in request_body:
        new_goal = Goal.from_dict(request_body)
        db.session.add(new_goal)
        db.session.commit()
        response_one_goal = {}
        response_one_goal["goal"] = Goal.to_dict(new_goal)
        return jsonify(response_one_goal), 201
    else:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

@goals_bp.route("/<goal_id>", methods=["GET"])
def read_one_goal(goal_id):
    goal = validate_goal(Goal, goal_id)
    response_one_goal = {}
    response_one_goal["goal"] = Goal.to_dict(goal)
    return jsonify(response_one_goal), 200

@goals_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_goal(Goal, goal_id)
    request_body = request.get_json()
    
    goal.update(request_body)

    goal.title = request_body["title"]

    db.session.commit()
    response_updated_goal = {}
    response_updated_goal["goal"] = Goal.to_dict(goal)
    return jsonify(response_updated_goal), 200

@goals_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_goal(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return make_response({"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"})

# @goals_bp.route("/<goal_id>/<completion>", methods=["PATCH"])
# def mark_goal_completed(goal_id, completion):
#     goal = validate_goal(Goal, goal_id)

#     if completion == "mark_complete":
#         goal.completed_at = datetime.now(timezone.utc)
#         goal.is_complete = True
#         send_message_to_slack(goal)

#     elif completion == "mark_incomplete":
#         goal.completed_at = None
#         goal.is_complete = False

#     db.session.commit()
#     response_updated_goal = {}
#     response_updated_goal["goal"] = Goal.to_dict(goal)
#     return jsonify(response_updated_goal), 200


# def send_message_to_slack(completed_goal):

#         # WAVE 4
#         # ID of channel you want to post message to
#         channel_id = "C04AL1N1AFJ"
#         SLACK_API_KEY = os.environ.get('API_KEY')
#         PATH = "https://slack.com/api/chat.postMessage"
#         slack_message_params = {
#                 "channel": channel_id, 
#                 "text": f"Someone just completed the goal {completed_goal.title}"}
#         # try:
#         #     # Call the chat.postMessage method using the WebClient
#         requests.post(PATH,
#                     data=slack_message_params,
#                     headers={"Authorization": SLACK_API_KEY}  
#         )