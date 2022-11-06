from app import db
from app.models.goal import Goal
from flask import Blueprint, jsonify, abort, make_response, request
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

bp = Blueprint("goals", __name__, url_prefix="/goals")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response(
            {"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


# CREATE
@bp.route("", methods=["POST"], strict_slashes=False)
def create_goal():
    try:
        request_body = request.get_json()
        new_goal = Goal.from_dict(request_body)
    except:
        abort(make_response(jsonify({
            "details": "Invalid data"}), 400))

    db.session.add(new_goal)
    db.session.commit()

    return make_response(jsonify({"goal": new_goal.to_dict()}), 201)


# READ ALL
@bp.route("", methods=["GET"], strict_slashes=False)
def read_all_goals():
    sort_query = request.args.get("sort")

    goal_query = Goal.query

    if sort_query == "asc":
        goal_query = goal_query.order_by(asc(Goal.title))
    if sort_query == "desc":
        goal_query = goal_query.order_by(desc(Goal.title))

    goals = goal_query.all()
    response_body = [goal.to_dict() for goal in goals]

    return make_response(jsonify(response_body), 200)


# READ ONE
@bp.route("/<goal_id>", methods=["GET"], strict_slashes=False)
def read_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()}), 200

# UPDATE ALL ONE
@bp.route("/<goal_id>", methods=["PUT"], strict_slashes=False)
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    return jsonify({"goal": goal.to_dict()}), 200

# UPDATE PART OF ONE
# @bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
# def mark_complete(task_id):
#     task = validate_model(Task, task_id)

#     task.completed_at = datetime.now()

#     db.session.commit()

#     # Send to SlackBot - consider using a helper function here
#     load_dotenv()
#     PATH = os.environ.get("COMPLETE_PATH")
#     PASS = os.environ.get("API_TOKEN")
#     query_params = {'text': f"Someone just completed the task {task.title}",
#                     'channel': 'U03QGU0M6K'}  # My DM for now
#     requests.post(PATH,
#                   json=query_params,
#                   headers={
#                       'Content-type': 'application/json',
#                       'Authorization': PASS
#                   })

#     return jsonify({"task": task.to_dict()}), 200

# UPDATE PART OF ONE
# @bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
# def mark_incomplete(task_id):
#     task = validate_model(Task, task_id)

#     task.completed_at = None

#     db.session.commit()

#     return jsonify({"task": task.to_dict()}), 200


#DELETE ONE TASK
@bp.route("/<goal_id>", methods=["DELETE"], strict_slashes=False)
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()
    return {
        "details": "Goal 1 \"Build a habit of going outside daily\" successfully deleted"
    }
